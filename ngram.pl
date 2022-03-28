#!/usr/bin/perl


=pod

Script that computes ngram probabilities.
Takes the ngram value as input from the terminal.
Reads poems from 'poems_all.txt'
and prints the probabilities.

Usage example:
perl ngram.pl 2
Output:
FROM_TOKENS\tTO_TOKENS\tPROBABILITY
la	noche	0.5
la	luna	0.5

=cut
$|++;

use strict;
use utf8;
use open ':std', ':encoding(UTF-8)';
binmode STDOUT, ":encoding(UTF-8)";

my $n = $ARGV[0];
my %ngram_prob;
my %ngram_count;
my %from_tok_count;
my $total = 0;
my %lines;
my $file_poems = "corpus/poems_all.txt";

# reading poems
open(my $fh, '<', $file_poems) or die "\nI cannot open file $file_poems\n";
	my $i = 0;
	while (my $line = <$fh>) {
		chomp($line);
		my @tokens = split(/ /, $line);
		$lines{$i} = \@tokens;
		$i++;
	}
close $fh;

if ($n == 1) {
	&unigram();
} else {
	&ngram()
}

sub unigram {
	for my $line (keys %lines) {
		my @tokens = @{$lines{$line}};
		for my $tok (@tokens) {
			# count ngram occurrences
			$ngram_count{$tok}++;
			# counting total occurrences
			$total++;
		}
	}
	# computing probabilities
	for my $ngram (keys %ngram_count) {
		$ngram_prob{$ngram} = $ngram_count{$ngram} / $total
	}
	# printing to stdout
	for my $ngram (keys %ngram_prob) {
		print "$ngram\t$ngram_prob{$ngram}\n";
	}
}

sub ngram {
	for my $line (keys %lines) {
		my @tokens = @{$lines{$line}};
		# adding beginning and end of line tokens
		unshift(@tokens, '<s>');
		push(@tokens, '</s>');

		# counting total occurrences
		for(my $i = 0; $i <= $#tokens - ($n-1); $i++) {
			# count ngram occurrences
			my @tok = @tokens[$i..($i+($n-1))];
			$ngram_count{join(' ', @tok)}++;

			# count ngram-1 occurrences
			my @from_tok = @tok[0..$n-1-1];
			my @to_tok = @tok[-1];
			$from_tok_count{join(' ', @from_tok)}++;
		}
	}

	# computing probabilities
	for my $ngram (keys %ngram_count) {
		my @tokens = split(/ /, $ngram);
		my $from_tok = join(' ', @tokens[0..$n-1-1]);
		my $to_tok = join(' ', @tokens[-1]);

		my $from_oc = $from_tok_count{$from_tok};
		my $ngram_oc = $ngram_count{$ngram};

		$ngram_prob{$from_tok}{$to_tok} = $ngram_oc/$from_oc;
	}

	# printing to stdout
	for my $from_tok (keys %ngram_prob) {
		for my $to_tok (keys %{$ngram_prob{$from_tok}}) {
			print "$from_tok\t$to_tok\t$ngram_prob{$from_tok}{$to_tok}\n";
		}
	}
}
