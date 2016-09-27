#!/usr/bin/perl -w
use strict;
use DBI ; 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# These are the database access parameters
my $driver = "DBI:ODBC:perlClass_formLetterData" ;
my $user = "perl";
my $password = "perl";
my $table = "CustomerTable";
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Get template as one string
open( DATA, $ARGV[0] ) ;
my @template = <DATA> ;               # How to do this...
my $template = join("",@template) ;   # ...in one step?
close( DATA ) ; 


# Get filter if present
my $filter = ( $ARGV[1] || "." )  ; 


# Get all records from db
my $dbh = DBI->connect($driver, $user, $password) || die "Couldn't connect to database: " . DBI->errstr();
my $stmt = "SELECT * FROM $table" ;
my $sh = $dbh->prepare($stmt) ; 
$sh->execute() || die "SQL Error" ;


# Try to substitute each keyword into each row
my $matches = 0 ;   # <<<<<< Breakpoint here and you won't get the "use of uninitialized value in substitution iteror" error (why?)
while( my $row = $sh->fetch() ) {
    
    # Ignore if record (first name, last name, or email) doesn't match filter <<<<< Ideally, factor this out (performance)
    next if not( @$row[1] =~ /$filter/i || @$row[2] =~ /$filter/i || @$row[4] =~ /$filter/i ) ;
    
    # Update match count
    $matches++ ; 
    
    # Build hash to map keywords to their db values
    my %map = {} ;
    $map{'$first_name$'}      =  @$row[1]  || '$remove$' ; 
    $map{'$last_name$'}       =  @$row[2]  || '$remove$' ; 
    $map{'$middle_initial$'}  =  @$row[3]  || '$remove$' ; 
    $map{'$email$'}           =  @$row[4]  || '$remove$' ; 
    $map{'$number_of_items$'} =  @$row[5]  || '$remove$' ; 
    $map{'$salutation$'}      =  @$row[7]  || '$remove$' ;


    # ...format as currency for these two
    if( @$row[6] ) {
        my $price = sprintf( "%1.2f", @$row[6] ) ;
        $map{'$price_per_item$'} = "\$$price" ;
        
        if( @$row[5] ) {
            my $total = sprintf( "%1.2f", @$row[5] * @$row[6] ) ;
            $map{'$total$'} = "\$$total" ; 
        } else {
            $map{'$total$'} = '$remove$' ; 
        }
    } else {
        $map{'$price_per_item$'} = '$remove$' ;
        $map{'$total$'} = '$remove$' ;         
    }
    
    # Expand a copy of the template and print it
    my $temp = $template ;
    $temp =~ s/(\$\w+\$)/$map{$1}/g ;                         # Perform substitutions <<<<< Cool re technique
    $temp =~ s/\s\$remove\$([\s\.])/$1 eq '.' ? '':' '/ge ;   # Remove the $remove$s
    print $temp ; 
}


# Status message
print "Done.  $matches matches.\n" ; 

# Close database connection
$dbh->disconnect();
