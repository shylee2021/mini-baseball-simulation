import argparse
import statistics

import bb_sim


def main(avg, N):
    batters = [bb_sim.Batter(avg=avg) for _ in range(9)]
    current = 0

    ground = bb_sim.Ground()

    s = []
    for _ in range(N):
        total_score = 0
        for inning in range(1, 10):
            n_outs = 0
            inning_score = 0
            while n_outs < 3:
                result = ground.simulate_one_pa(batters[current])
                inning_score += result.scores
                n_outs += result.outs

                current = current + 1 if current < 8 else 0

            ground.end_inning()
            # print(f"{inning} inning: {inning_score} score")

            total_score += inning_score

        # print(f"total: {total_score} score")
        s.append(total_score)

    print(
        f"mean={statistics.mean(s):.3f}, std={statistics.stdev(s):.3f}, max={max(s)}, min={min(s)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--avg", help="batting average", type=float)
    parser.add_argument("--N", help="number of repeat", type=int)
    args = parser.parse_args()

    main(args.avg, args.N)
