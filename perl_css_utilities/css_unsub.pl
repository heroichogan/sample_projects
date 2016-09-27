#!/usr/bin/perl -w
use strict;

my $line = <STDIN> ;
$line =~ s/^.*\/\*(.+?)\*\/.*$/$1/g ; 
print $line ; 