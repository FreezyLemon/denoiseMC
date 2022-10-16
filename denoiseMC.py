def denoiseMC(clip, denoise_fn, radius: int = 2, search: int = 3, blksize: int = 16):
    from vapoursynth import core
    mv = core.mv
    std = core.std

    if clip is None:
        raise ValueError('clip is required')

    if denoise_fn is None:
        raise ValueError('denoise_fn is required')

    if radius < 1:
        raise ValueError('radius must be greater than 0')

    sup = mv.Super(clip, hpad=blksize, vpad=blksize)

    vecs = []
    for d in range(radius, 0, -1):
        vecs.append(mv.Analyse(sup, isb=True , blksize=blksize, overlap=blksize/2, delta=d, search=search, truemotion=True))

    for d in range(1, radius + 1):
        vecs.append(mv.Analyse(sup, isb=False, blksize=blksize, overlap=blksize/2, delta=d, search=search, truemotion=True))

    # Refine MVs with Recalculate() at half block size
    if blksize > 4:
        vecs = map(lambda v: mv.Recalculate(sup, v, blksize=blksize/2, overlap=blksize/4, search=search, truemotion=True), vecs)

    mcomped = list(map(lambda r: mv.Flow(clip, sup, r), vecs))
    interleaved = std.Interleave(clips=mcomped[:radius] + [clip] + mcomped[radius:])

    # denoise_fn must return a clip
    denoised = denoise_fn(interleaved)
    if denoised is None:
        raise ValueError('denoise_fn does not return a value when called')

    return std.SelectEvery(denoised, cycle=radius * 2 + 1, offsets=[radius])
