# denoiseMC - Motion-compensated denoising, based on MVTools

```python
def denoiseMC(clip, denoise_fn, radius: int = 2, search: int = 3, blksize: int = 16):
```

`denoise_fn` takes only one parameter, the input video clip. If `blksize` is 8 or higher, the motion vectors are recalculated at half `blksize` after the initial analysis.

## Examples

Usage via defined function:

```python
from denoiseMC import denoiseMC

def denoise(clip):
    return core.ttmpsm.TTempSmooth(clip, maxr=4)

denoised = denoiseMC(clip, radius=4, denoise_fn=denoise)
```

Lambdas are also possible:

```python
from denoiseMC import denoiseMC

denoised = denoiseMC(clip, lambda c: core.ttmpsm.TTempSmooth(c))
```
