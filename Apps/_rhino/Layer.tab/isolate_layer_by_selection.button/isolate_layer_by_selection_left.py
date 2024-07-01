
__alias__ = "IsolateLayerBySelection"
__doc__ = "This button does IsolateLayerBySelection when left click"
import rhinoscriptsyntax as rs

def isolate_layer_by_selection():
    ids = rs.SelectedObjects(include_lights = True, include_grips = False)
    if not ids: return
    rs.EnableRedraw(False)

    used_layers = set()
    obj_by_layers = []
    for id in ids:
        layer = rs.ObjectLayer(id)
        used_layers.add(layer)

    for layer in list(used_layers):
        obj_by_layers.extend(rs.ObjectsByLayer(layer, True))

    invert_objs = rs.InvertSelectedObjects(include_lights = True)
    rs.HideObjects(invert_objs)


    rs.UnselectObjects(obj_by_layers)