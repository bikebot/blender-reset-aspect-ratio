bl_info = {
    "name": "Reset Aspect Ratio",
    "author": "Bikebot",
    "version": (1, 0, 3),
    "blender": (2, 78, 0),
    "location": "Sequencer > Reset Aspect Ratio",
    "description": "Correct aspect ratio of image and video strips",
    "warning": "",
    "category": "Sequencer"
}

import bpy

class ResetAspectRatio(bpy.types.Operator):
    """Correct aspect ratio of image and video strips"""
    bl_idname = "scene.reset_aspect_ratio"
    bl_label = "Reset Aspect Ratio"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        strip = context.selected_editable_sequences[0]
        return strip.type == 'TRANSFORM'

    def execute(self, context):
        transform_strip = context.selected_editable_sequences[0]
        base_strip = transform_strip.input_1
        while base_strip.type == 'META' and len(base_strip.sequences):
            base_strip = base_strip.sequences[0]
        if base_strip.type not in ('IMAGE', 'MOVIE'):
            return {'CANCELLED'}
        elem = base_strip.elements[0]
        orig_width = elem.orig_width
        orig_height = elem.orig_height
        if base_strip.use_crop:
            orig_width -= base_strip.crop.min_x + base_strip.crop.max_x
            orig_height -= base_strip.crop.min_y + base_strip.crop.max_y
        render = context.scene.render
        
        if base_strip.use_translation:
            base_strip.use_translation = False 
        #self.report({'INFO'}, 'use_translation={:}'.format(image_strip.use_translation))
        transform_strip.use_uniform_scale = False
        scale_factor_y = render.resolution_y / orig_height
        scale_factor_x = render.resolution_x / orig_width
        scale_factor = min(scale_factor_x, scale_factor_y)
        fitScale = transform_strip.fitScale
        target_width = orig_width * scale_factor * fitScale/100
        target_height = orig_height * scale_factor * fitScale/100
        transform_strip.scale_start_x = target_width / render.resolution_x
        transform_strip.scale_start_y = target_height / render.resolution_y

        return {'FINISHED'}


def FitPanel(self, context):
    layout = self.layout
    obj = context.selected_editable_sequences[0]
    layout.prop(obj, "fitScale")
    layout.operator("scene.reset_aspect_ratio", icon="FULLSCREEN_EXIT")


def register():
    bpy.types.TransformSequence.fitScale = bpy.props.FloatProperty(
        name="Fit Scale", description="Uniform scale of fitted image", default=100, 
        min=0.0, soft_max=1000, subtype="PERCENTAGE", update=ResetAspectRatio.execute)
    bpy.utils.register_class(ResetAspectRatio)
    bpy.types.SEQUENCER_PT_effect.append(FitPanel)

# Unregister doesn't seem to work properly
def unregister():
    del bpy.types.TransformSequence.fitScale
    bpy.types.SEQUENCER_PT_effect.remove(FitPanel)
    bpy.utils.unregister_class(FitImage)

if __name__ == "__main__":
    register()
