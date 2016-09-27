#!/usr/bin/perl -w
use strict ;
use DBI ; 



# These are the database access parameters
my $driver = "DBI:ODBC:perlClass_formLetterData" ;
my $user = "perl";
my $password = "perl";
my $table = "CustomerTable";


# Get command line argument
my @fields = split( /:/, $ARGV[0] ) ;
die "Wrong number of fields specified in input.  Error" if scalar @fields != 7 ; 


# Get handle to db
my $dbh = DBI->connect($driver, $user, $password) || die "Couldn't connect to database: " . DBI->errstr();


# Check for duplicate records (of course, we're guessing here)
my $stmt = "SELECT * FROM $table WHERE first_name='$fields[0]' AND last_name='$fields[1]' AND middle_initial='$fields[2]'" ;
my $rows = $dbh->selectall_arrayref($stmt) || die "SQL error" ; 
if( scalar @$rows > 0 ) { 
    print "Record already in database (first_name=$fields[0], last_name=$fields[1], middle_initial=$fields[2]).  Aborting insert." ;
    exit ; 
}


# Get next available key <<<<< Ideally would find a better function to call--one to return a scalar
$stmt = "SELECT MAX(id) FROM $table" ;
my @aRows = $dbh->selectall_arrayref($stmt) || die "SQL error" ;
my $id = $aRows[0][0][0];
$id ++ ; 


# Remove desired record from database
$stmt = "INSERT INTO $table (id, first_name, last_name, middle_initial, email, number_of_items, price_per_item, salutation) VALUES ('$id', '$fields[0]', '$fields[1]', '$fields[2]', '$fields[3]', '$fields[4]', '$fields[5]', '$fields[6]' )" ; 
$dbh->do($stmt) || die "SQL error" ;    


# Close file and database connection
$dbh->disconnect();


# Print message
print "Done inserting new record." ;
