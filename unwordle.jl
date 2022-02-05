#!/usr/bin/env -S julia -t4 --startup-file=no 
#-e 'using DaemonMode; runargs()'
using Statistics
using ArgParse

word_diff(A, B) = sum(3^i * if a==b; 1 elseif a in B; 2 else 3 end for (i, (a,b)) in enumerate(zip(A, B)))

word_diff1(A,B) = join(if a==b; a; elseif a in B; '+' else '-' end for (a,b) in zip(A,B))

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
	guess=nothing;
	score=mean_group_size, 
	input=stdin, 
	output=stdout
	)
	function try_word(word) 
		println(output, word)
		flush(output)
	end

	function pick_word(words) 
		(word_score, index) = findmin(w-> score(w, words), word_list)
		@debug "" index word_list[index]
		return word_list[index]
	end
	
	if guess == nothing
		guess = pick_word(word_list)
	end

	try_word(guess)
	guesses = 1

	candidates = copy(word_list)
	@debug " " length(candidates) guesses

	for result in eachline(input)
		filter!(w-> word_diff1(guess, w) == result, candidates)
		@debug " " guesses ifelse(length(candidates) < 10, candidates,length(candidates))

		if isempty(candidates)
			error("ran out of words to guess from")
		elseif length(candidates) == 1
			guess = only(candidates)
		else
			guess = pick_word(candidates)
		end
		try_word(guess)
		guesses += 1
	end
	return (word=guess, guesses=guesses)
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
	result = unwordle(readlines(args["word-list"]), args["guess"])
	join(stderr, result, " ")
	println(stderr)
end

main()
