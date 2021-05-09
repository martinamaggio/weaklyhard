# WeaklyHard

This library implements basic weakly-hard constraint analysis using python.
It is tested using `python3` and (on purpose) does not use any support from
external libraries like `numpy`. The library uses `itertools`, which is part
of the standard python library.

### Basic usage and definitions

We denote with the term _window_ a sequence of consecutive events or
realisations (i.e., deadline hits or misses). A deadline hit is represented
with a `1` and a deadline miss is represented with a `0`.

The library supports five types of constraints.

1. _Any-Miss_ constraint `AM_Constraint(x, w)` <br>
   In every window of length `w`, there are
   _at most_ `x` deadline misses.
2. _Any-Hit_ constraint `AH_Constraint(x, w)` <br>
   In every window of length `w` there are
   _at least_ `x` deadline hits.
3. _Row-Miss_ constraint `RM_Constraint(x)` <br>
   In the entire sequence there are
   _at most_ `x` consecutive deadline misses.
   The window size here is irrelevant.
4. _Row-Hit_ constraint `RH_Constraint(x)` <br>
   In every window of length `w` there are
   _at least_ `x` consecutive deadline hits.
5. _Row-2_ constraint `R2_Constraint(x, w)` <br>
   A sequence can contain either deadline hits, or a number of misses `m`,
   upper-bounded by `x`, followed by a number of hits that is exactly
   `w-m`.

The first four types of constraints are defined and analysed in

> G. Bernat, A. Burns, A. Liamosi; _Weakly hard real-time systems_;
> IEEE Transactions on Computers; Volume 50; Issue 4;
> [doi: 10.1109/12.919277](https://doi.org/10.1109/12.919277).

The last type of constraint is introduced in

> N. Vreman, A. Cervin, M. Maggio; _Stability and Performance Analysis
> of Control Systems Subject to Bursts of Deadline Misses_;
> Euromicro Conference on Real-Time Systems (ECRTS) 2021.

For every constraint `c`, the library contains two functions:

    c.gen_sequence(size: int)
    c.check_sequence(sequence: list of int)

* `gen_sequence` generates a (random) sequence of length `size` that
  satisfies the specific constraint `c`,
* `check_sequence` checks a sequence against the constraint returning
  `True` or `False` depending on the sequence satisfying the constraint.
