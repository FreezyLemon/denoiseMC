# denoiseMC - Motion-compensated denoising, based on MVTools

This script requires [MVTools](https://github.com/dubhater/vapoursynth-mvtools).

```python
def denoiseMC(clip, denoise_fn, radius: int = 2, search: int = 3, blksize: int = 16):
```

## Parameters

`denoise_fn` is a function accepting one parameter (the video clip to denoise). Check the examples to understand how to use this parameter.

`radius` sets the temporal radius for motion compensation.

`blksize` sets the block size for MVTools' `Analyse` function. If blksize is 8 or larger, the motion vectors will be recalculated with `blksize/2` to get finer results.

`search` sets the search mode for MVTools' `Analyse` and `Recalculate` functions.

## Examples

Usage via defined function:

```python
from denoiseMC import denoiseMC

def denoise(clip):
    return core.ttmpsm.TTempSmooth(clip, maxr=4)

# Make sure to set radius=4 so TTempSmooth can use maxr=4
denoised = denoiseMC(clip, radius=4, denoise_fn=denoise)
```

Lambdas are also possible:

```python
from denoiseMC import denoiseMC

denoised = denoiseMC(clip, lambda c: core.ttmpsm.TTempSmooth(c))
```

## How it works

This script creates a sequence of motion-compensated frames around each source frame, and then runs your denoising function on this sequence of frames. The motion-compensated frames are then discarded and only the (now denoised) source frame is returned.
