#!/usr/bin/env -S julia -t4 --startup-file=no 
#-e 'using DaemonMode; runargs()'
using Statistics
using ArgParse

word_diff(A, B) = sum(3^i * if a==b; 1 elseif a in B; 2 else 3 end for (i, (a,b)) in enumerate(zip(A, B)))

parse_diff(s) = sum(3^i * if a=='-'; 3 elseif a=='+'; 2; else 1 end for (i, a) in enumerate(s))

freq(data) = (sum(==(x), data) for x in unique(data))

negative_num_groups(word, words) = -length(unique(word_diff.(word, words)))

group_sizes(word, words) = freq(word_diff.(word,words))

mean_group_size(word, words) = mean(group_sizes(word, words))

max_group_size(word, words) = maximum(group_sizes(word,words))

expected_group_size(word, words) = mean(group_sizes(word,words).^2)

entropy(word, words) = let W = length(words);  sum(S/W * log(S/W) for S in group_sizes(word,words)) ; end

function unwordle(
	word_list, 
	guess, 
	score=negative_num_groups, 
	input=stdin, 
	output=stdout
	)
	function try_word(word) 
		println(output, word)
		flush(stdout)
	end

	pick_word(words) = words[last(findmin(w-> score(w, words), words))]
	
	if guess == nothing
		guess = pick_word(word_list)
	end

	try_word(guess)
	guesses = 1

	candidates = copy(word_list)

	for result in eachline(input)
		filter!(w-> word_diff(guess, w) == parse_diff(result), candidates)
		if isempty(candidates)
			try_word("tares")
			return ("failed", -guesses)
		elseif length(candidates) == 1
			guess = only(candidates)
		else
			guess = pick_word(candidates)
		end
		try_word(guess)
		guesses += 1
	end
	return (guess, guesses)
end


function main()
	parser = ArgParseSettings()
	@add_arg_table parser begin
		"--guess", "-g"
			help = "the initial guess"
			default = nothing
			arg_type = Union{Nothing, String}
		 "--word-list", "-f"
		help="word list text file"
		default = "./wordles.txt"
	end
	args = parse_args(parser)
	join(stderr, unwordle(readlines(args["word-list"]), args["guess"]), " ")
	println(stderr)
end

main()
