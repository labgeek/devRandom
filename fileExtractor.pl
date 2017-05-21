#!/usr/bin/perl
#######################################################################
# Created on:  01/12/08
# File:        fileExtractor.pl
# Description: wrapper program that calls a program called foremost
# and takes the output of that program and redirects it into directories
# for your use.
#
######################################################
use Getopt::Std;
use File::Find;
use File::Basename;
use File::Copy;


my (%opt, %sigs) = ();

# use flag options
getopts( "hd:f:o:", \%opt );
my $sigfile = "headersig\.txt";

my ( $sigfileread, $htmcounter, $gifcounter, $zipcounter, $jpgcounter, $execounter ) = 0;

#required use of -d for directory name
unless ( $opt{d} ) { printUsage(); }
if     ($opt{h})    { printUsage(); }
if ( defined $opt{d} && defined $opt{o} ) {
	if ( -e $sigfile ) {
		if ( readsigfile($sigfile) ) {
			print "Signature file sucessfully read - continuing\n";
			$sigfileread = 1;
			foreach ( keys %sigs ) {
				my @list = @{ $sigs{$_} };
			}
		}
	}
	else {
		print "Signature file not read\n";
	}    
	find( \&search,      $opt{d} );
	print "NOW,locating files....\n";
	find( \&locateFiles, $opt{o} );
	open( STATS, ">$opt{o}statstics.txt" );
	printf STATS "%-30s\t%s\n", "Total number of EXE files", $execounter;
	printf STATS "%-30s\t%s\n", "Total number of GIF files", $gifcounter;
	printf STATS "%-30s\t%s\n", "Total number of JPG files", $jpgcounter;
	printf STATS "%-30s\t%s\n", "Total number of ZIP files", $zipcounter;
	printf STATS "%-30s\t%s\n", "Total number of HTM files", $htmcounter;
	close(STATS);
}

# Subroutines below
# Verifies that the files are tcpdump files, then runs foremost on them printing the output
# to our specified output directory
sub search {
	 $fpath = $File::Find::name;
	 $fname = basename($fpath);

	
	if ( $fname =~ /log*/ ) {
		$outcounter++;
		my $out = "output" . $outcounter;
		open( FOR, "/usr/bin/foremost -i $fpath -o $opt{o}/$out |" );
	}
}

# locates EXE, GIF, ZIP, HTM, and JPG files
sub locateFiles {
	my $fpath   = $File::Find::name;
	my $fname   = basename($fpath);
	my $dest    = $opt{o} . $fname;
	my $exe     = $opt{o} . "EXE";
	my $gif     = $opt{o} . "GIF";
	my $zip     = $opt{o} . "ZIP";
	my $htm     = $opt{o} . "HTM";
	my $jpg     = $opt{o} . "JPG";
	my $unknown = $opt{o} . "unknown";
	if ( $fname =~ /.exe/ ) {
		mkdir $exe unless -d $exe;
		copy( $fpath, $exe ) or die "Copy failed: $!";
		$execounter++;
	}
	elsif ( $fname =~ /.gif/ ) {
		mkdir $gif unless -d $gif;
		copy( $fpath, $gif ) or die "Copy failed: $!";
		$gifcounter++;
	}
	elsif ( $fname =~ /.htm/ ) {
		mkdir $htm unless -d $htm;
		copy( $fpath, $htm ) or die "Copy failed: $!";
		$htmcounter++;
	}
	elsif ( $fname =~ /.zip/ ) {
		mkdir $zip unless -d $zip;
		copy( $fpath, $zip ) or die "Copy failed: $!";
		$zipcounter++;
	}
	elsif ( $fname =~ /.jpg/ ) {
		mkdir $jpg unless -d $jpg;
		copy( $fpath, $jpg ) or die "Copy failed: $!";
		$jpgcounter++;
	}
	else {

	}
}

# prints the usuage for us
sub printUsage {
	print "Usage:\tfileExtractor -[d] <directory> -[o] <output filename>\n";
	print "\tDate:  01/16/08 \n";
	print "\nOptions:\n";
	print "\t-h - print help (optional)\n";
	print "\t-d - input directory (required)\n";
	print "\t-o - output directory(required)\n";
	exit;
}

# reads the header signature file to later file verification
sub readsigfile {
	my $file = shift;
	if ( -e $file ) {
		open( FH, $file ) || die " Could not open $file : $! \n ";
		while (<FH>) {

			# skip lines that begin w/ # or are blank
			next if ( $_ =~ m/^#/ || $_ =~ m/^\s+$/ );
			chomp;
			my ( $sig, $tag ) = ( split( /,/, $_, 3 ) )[ 0, 1 ];
			my @list = split( /;/, $tag );    # split on ";
			foreach (@list) {
				$_ =~ s/\s//;                 #remove space
				$_ =~ s/\.//;                 # remove period
			}

			# %sigs is a global variable
			$sigs{$sig} = [@list];
		}
		close(FH);
		return 1;
	}
	else {
		return undef;
	}
}
