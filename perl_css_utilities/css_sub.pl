#!/usr/bin/perl -w
use strict;

my $newRule = join( " ", @ARGV ) ; 
my $line = <STDIN> ;
$line =~ s/(^.+$)/$newRule \/\*$1\*\//g ; 
print $line ; 