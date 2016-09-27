#!/usr/bin/perl -w
use strict;

# Get entire selection
my $line = "";
while( <STDIN> ) {
    $line .= $_ ; 
}

# Get all matches
my @matchesQuoted   = $line =~ /(?:id|class)\s*=\s*['"](.+?)['"]/gis ;
my @matchesUnquoted = $line =~ /(?:id|class)\s*=\s*([^'"]+?)[\s>]/gis ;
    
    
# Return now if no matches
if( scalar @matchesQuoted == 0 && scalar @matchesUnquoted == 0 ) { 
    print "Nothing matched";
    exit();
}


# Remove duplicate matches
my %uniqueMatches ;
foreach( @matchesQuoted, @matchesUnquoted ) {
    $uniqueMatches{ $_ } = "" ;
}


# Print unique matches
print join ", ", sort keys %uniqueMatches ; 