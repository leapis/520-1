import advanced_agent as adv
import basic_agent as basic
import minesweeper

if __name__ == '__main__':
    runs = 5000
    basic_expl = 0
    basic_guessed = 0
    adv_expl = 0
    advanced_guessed = 0
    inference_usage = 0
    for run in range(runs):
        if (run % int(runs / 10) == 0): print(run / int(runs / 10) * 10,"%")
        current_iteration_guess_basic = 0
        current_iteration_guess_adv = 0
        grid = minesweeper.generate_environment(40, 150)
        expl, guess = basic.sweep_grid(grid)
        current_iteration_guess_basic = guess
        basic_expl, basic_guessed = basic_expl + expl, basic_guessed + guess
        expl, guess, infer = adv.sweep_grid(grid)
        current_iteration_guess_adv = 0
        adv_expl, advanced_guessed, inference_usage = adv_expl + expl, advanced_guessed + guess, inference_usage + infer
        assert (current_iteration_guess_basic > 0 or current_iteration_guess_adv <= current_iteration_guess_basic), "WEIRDGUESS"
    print ("basic:", basic_expl)
    print ("basic_g:", basic_guessed)
    print ("adv:", adv_expl)
    print ("adv_g:", advanced_guessed)
    print ("inferences:", inference_usage)
