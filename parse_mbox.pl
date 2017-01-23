#!/usr/bin/perl
#######################################################################
# Created on:  October 8th, 2007
# File:        parse_mbox.pl
# Description: A script that parses AOL specific email headers to
# provide the following information:
#
# @author(s) JD Durick
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, using version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
######################################################

use strict;
use MIME::Base64;
use Getopt::Std;
use Date::Parse;
use lib '/data/GeoIP';
my $GEOPATH = '/data/GeoIP';
my $orgdat =
  Geo::IP::PurePerl->new( "$GEOPATH/GeoIPOrg.dat", 'GEOIP_STANDARD' );
my $gi = Geo::IP::PurePerl->new( "$GEOPATH/GeoIPCity.dat", 'GEOIP_STANDARD' );
my $dom =
  Geo::IP::PurePerl->new( "$GEOPATH/GeoIPDomain.dat", 'GEOIP_STANDARD' );
my (
	 $countrycode, $countrycode3, $countryname, $region,
	 $city,        $postal,       $lat,         $lon,
	 $dma,         $areacode,     $org
) = "";
use PurePerl;
my @header            = ();
my (%opt)             = ();
my $results_array_ref = "";
my $counter           = 0;
getopts( "hf:o:", \%opt );
unless ( $opt{f} ) { printUsage(); }
if     ( $opt{h} ) { printUsage(); }
open( MBOX, "<$opt{f}" );
$results_array_ref = parse_file( $opt{f} );
open( OUTPUT, ">>$opt{o}" );

foreach my $header_string (@$results_array_ref) {

	#	print "$header_string\n";
	$counter++;
	my $header_hash_ref = parse_header($header_string);
	if ( !defined $header_hash_ref ) {
		next;
	}
	else {
		(
		   $countrycode, $countrycode3, $countryname, $region,
		   $city,        $postal,       $lat,         $lon,
		   $dma,         $areacode
		) = $gi->get_city_record( $header_hash_ref->{'received'} );
		$org = $orgdat->org_by_name( $header_hash_ref->{'received'} );
		print OUTPUT
"$header_hash_ref->{'from'}, $header_hash_ref->{'to'}, $header_hash_ref->{'subject'}, $header_hash_ref->{'date'}, $header_hash_ref->{'decimaldate'}, $header_hash_ref->{'clen'}, $header_hash_ref->{'received'}, $org, $city, $region, $countryname\n";
	}
}
close MBOX;
close OUTPUT;
print "total number of headers:  $counter\n";

#----------------------------------

######################################################################
# Description:  parses out data within mbox
# Input/Output:  array ref input
# Return value:  hash ref - output
######################################################################

sub parse_header {
	my $header      = shift;
	my %header_hash = ();
	my @header      = split( /\n/, $header );
	for ( my $i = 0 ; $i < @header ; $i++ ) {
		my $line = $header[$i];
		if ( $line =~ /^Received: /i ) {
			if ( $line =~
				 /^Received: from \[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]/ )
			{
				$header_hash{'received'} = $1;
			}
		}
		if ( $line =~ /^From: / ) {
			if (
				$line =~ /\b([A-Za-z_%+0-9]+@[A-Z0-9a-z._]+\.[A-Za-z]{2,4})\b/ )
			{
				$header_hash{'from'} = $1;
			}
		}
		if ( $line =~ /^To: / ) {
			if (
				$line =~ /\b([A-Za-z_%+0-9]+@[A-Z0-9a-z._]+\.[A-Za-z]{2,4})\b/ )
			{
				$header_hash{'to'} = $1;
			}
		}
		if ( $line =~ /^Subject: (.*)$/i ) {
			$header_hash{'subject'} = $1;
		}
		if ( $line =~ /^Content-Length: (.*)$/i ) {
			$header_hash{'clen'} = $1;

			#		print "clen = $1\n";
		}
		if ( $line =~ /^(?:Date|Sent):(.*?)\s*$/i ) {
			my $date = str2time($1);
			$header_hash{'date'}        = $1;
			$header_hash{'decimaldate'} = $date;
		}
	}
	return \%header_hash;
}

######################################################################
# Description:  Prints the usage of the perl script.
# Input/Output:  no input or output
# Return value:  exits out (return 0)
######################################################################

sub printUsage {
	print "Usage:\parse_mbox.pl -[f] <File name>\n";
	print "\tDate:  09/22/07 - <jdurick\@mitre.org>\n";
	print "\nOptions:\n";
	print "\t-h - print help (optional)\n";
	print "\t-f - mbox filename\n";
	print "\t-o - output filename (comma delimited)\n";
	exit;
}

######################################################################
# Description:  cleans up the mbox input, pushes everything into an array
# Input/Output:  pass in the input filename
# Return value:  returns hash ref
######################################################################

sub get_contents {
	my $file = shift;
	my @return;
	open( FILE, "<$file" ) || die "can't open file: $!\n";
	while (<FILE>) {
		chomp;
		s/(\15|\32|\^M|
)//g;
		push( @return, $_ );
	}
	close FILE;
	return \@return;
}
######################################################################
# Description:  uses regex to parse out header contents
# Input/Output: input filename
# Return value:  exits out (return 0)
######################################################################

sub parse_file {
	my $file = shift;
	my @return;
	my $file_contents   = get_contents($file);
	my $start_of_header = 0;
	my $end_of_header   = 0;
	for ( my $i = 0 ; $i < @$file_contents ; $i++ ) {
		if (
			 $start_of_header == 0
			 || (    $$file_contents[ $i - 1 ] =~ /^\s*$/
				  && $$file_contents[$i] !~ /^\s*$/ )
		  )
		{
			for ( my $end = $i + 1 ; $end < @$file_contents ; $end++ ) {
				if (    $$file_contents[$end] =~ /^\s*$/
					 || $end == @$file_contents - 1 )
				{

					#print "filecontents[$end] =  $$file_contents[$end]\n";
					my $header_chunk = '';
					for ( my $start = $i ; $start < $end ; $start++ ) {
						$header_chunk .= "$$file_contents[$start]\n";
					}
					if ( $header_chunk =~ /\nFrom /i ) {
						push( @return, $header_chunk );
					}
					if ( $header_chunk =~ /\n[0-9a-zA-Z\+\/=]{20,}/ ) {

						#print "hcunk = $header_chunk\n";
					}
					if (
						 ( $header_chunk =~ /\n[0-9a-zA-Z\+\/=]{20,}/ )
						 || ( $header_chunk =~
							  /\nContent-Disposition: attachment;/i )
					  )
					{

						#		print "headerchunk = $header_chunk\n";
					}
					$i = $end;
				}
			}
		}
	}
	return \@return;
}
__END__
