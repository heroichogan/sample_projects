#!/usr/bin/perl -w
use strict;

# Get entire selection
my $line = "";
while( <STDIN> ) {
    $line .= $_ ; 
}

# Get all matches
my @matches = $line =~ /<(\w+?)[\s>]/gs ;  


# Return now if no matches
if( scalar @matches == 0 ) { 
    print "Nothing matched";
    exit();
}


# Remove duplicate matches
my %uniqueMatches ;
foreach( @matches ) {
    $uniqueMatches{ $_ } = "" ;
}


# Print unique matches
print join ", ", sort keys %uniqueMatches ; 