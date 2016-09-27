#!/usr/bin/perl -w
use strict;
use DBI;

# 
# Recommended fields
# 
#     first_name
#     last_name
#     middle_initial
#     email
#     number_of_items
#     price_per_item
#     salutation
# 


# These are the database access parameters
my $driver = "DBI:ODBC:perlClass_formLetterData" ;
my $user = "perl";
my $password = "perl";


# Create AddressBook table
my $table = "CustomerTable";
my $dbh = DBI->connect($driver, $user, $password) || die "Couldn't connect to database: " . DBI->errstr();
my $stmt = "CREATE TABLE $table (id int PRIMARY KEY, first_name VARCHAR(64), last_name CARCHAR(64), middle_initial VARCHAR(1), email VARCHAR(64), number_of_items INT, price_per_item REAL, salutation VARCHAR(2) )";
$dbh->do($stmt);


# Close file and database connection
$dbh->disconnect();



