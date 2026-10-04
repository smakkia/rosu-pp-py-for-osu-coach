"""Sanity check for the built wheel: the new osu! fields are there and the gradual calculator gives, after every
object, the same pp as a full calculation of that many objects (osu!stable scores, as osu-coach uses them)."""

import rosu_pp_py as rosu

bm = rosu.Beatmap(path="tests/fixtures/test_map.osu")
worst = 0.0
for mods in (0, 16, 8 + 64):
    gradual = rosu.GradualPerformance(rosu.Difficulty(mods=mods, lazer=False), bm)
    for k in range(1, bm.n_objects + 1):
        full = rosu.Performance(mods=mods, lazer=False, passed_objects=k, misses=1 if k > 10 else 0).calculate(bm)
        step = gradual.next(full.state)
        worst = max(worst, abs(full.pp - step.pp))
    print(f"mods={mods}: {full.pp:.3f}pp (reading {full.pp_reading:.3f}pp), {full.difficulty.stars:.3f}*, "
          f"reading {full.difficulty.reading:.3f}, reading notes {full.difficulty.reading_difficult_note_count:.3f}")

print(f"largest gradual/full difference: {worst}")
assert worst < 1e-6, "the gradual calculator disagrees with the full calculation"
