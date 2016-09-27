#!/usr/bin/perl -w
use strict ;
use DBI ; 



# These are the database access parameters
my $driver = "DBI:ODBC:perlClass_formLetterData" ;
my $user = "perl";
my $password = "perl";
my $table = "CustomerTable";


# Get command line argument
my $id = $ARGV[0] ; 


# Get db handle
my $dbh = DBI->connect($driver, $user, $password) || die "Couldn't connect to database: " . DBI->errstr();


# Remove desired record from database
my $stmt = "DELETE FROM $table WHERE (id = $id)" ; 
my $rows = $dbh->do($stmt) || die "SQL error (no match for id=$id).  Error" ;    


# Close file and database connection
$dbh->disconnect();


# Print message
print "Done deleting record $id." ;
print "  (That record wasn't in the database.)" if scalar $rows == 0 ; 

