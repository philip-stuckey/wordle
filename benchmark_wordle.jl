#!/usr/bin/env -S julia -t3 --startup-file=no 
include("unwordle.jl")

using ArgParse

function wordle(word, word_list; input, output)
	for guess in eachline(input)
		@debug "" guess
		if guess == word
			@debug "you won!", word
			flush(input)
			close(input)
			flush(output)
			close(output)
			return
		else
			@debug "incorrect"
			println(output, word_diff(guess, word))
		end
	end
end

function main()
	word_list = readlines("wordles.txt")
	score = mean_group_size
	
	@info "finding initial word"
	initial_results  = (value=(word="tares",),) # @timed unwordle(word_list; score, input=devnull, output=devnull)
	@info "" initial_results

	initial_guess = initial_results.value.word

	for word in  word_list # ("babes",) 
		guesses = IOBuffer()
		results = IOBuffer()
		unwordle_task = @task begin 
			@debug "got here"
			result = @timed unwordle(word_list, initial_guess; score, input=results, output=guesses) 
			@show  result.value.word result.value.guesses result.time
		end

		wordle_task = @task begin
			wordle(word, word_list, input=guesses, output=results)
		end

		schedule(unwordle_task)
		schedule(wordle_task)
		@debug "" unwordle_task istaskstarted(unwordle_task)
		@debug "" wordle_task istaskstarted(unwordle_task)

		wait(wordle_task)
		wait(unwordle_task)

		@debug unwordle_task
	 end
end

if abspath(PROGRAM_FILE) == @__FILE__
    # do something only this file is executed. 
	main()
end
