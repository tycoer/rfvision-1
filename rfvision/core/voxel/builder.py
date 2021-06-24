import robotflow.rflib as rflib

from . import voxel_generator


def build_voxel_generator(cfg, **kwargs):
    """Builder of voxel generator."""
    if isinstance(cfg, voxel_generator.VoxelGenerator):
        return cfg
    elif isinstance(cfg, dict):
        return rflib.runner.obj_from_dict(
            cfg, voxel_generator, default_args=kwargs)
    else:
        raise TypeError('Invalid type {} for building a sampler'.format(
            type(cfg)))