#!/usr/bin/perl
#######################################################################
# Created on:  March 02, 2007
# File:        verifyChecksum.pl
# Version:	   0.1
#
# Description: Script to verify whether or not the MD5/SHA256 checksums
# of the gzipped packet capture files created by packet sniffers are
# accurate and match their corresponding .info metadata file entries.
# These checksums apply to both pre-compression and post-compression
# files.
#
# @author: JD Durick
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
#######################################################################

# TODO
# proper POD documentation
# inline testing (if want to be anal)
# command-line options for ease of use
# OO-ify into packages to satisfy absurd requirement downtown :)
# print all data to file (log), just pipe it dude

# SVN:
# $Id: verifyChecksum.pl 73 2007-03-17 16:45:04Z root $
# $Date: 2007-03-17 11:45:04 --500 (Sat, 17 Mar 2007) $
# $URL: file:///svn/trunk/ValidateHash/verifyChecksum.pl $
# $Rev: 73 $


#Quick note
# wrote this script while playing nl holdem online so
# it probably could be better :) - but then
# again, its just a small utility for verfiying hash
# checksums between .gz and metadata files...jd


# List the packages we need here...
use Digest::SHA qw(sha1 sha1_hex sha1_base64);
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Getopt::Long;
use Carp;
use Time::HiRes qw(gettimeofday);
use File::Basename;
use Getopt::Std;
use FileHandle;
use Compress::Zlib;
require "find.pl";


# declarations
my $start = gettimeofday;
@info     = ();
@gzipped  = ();
@suffixes = qw(.info);
$counter  = 0;
my $gzfiles       = 0;
my $infofiles     = 0;
my $totalfiles    = 0;
my %optctl        = ();
my $containMD5    = 0;
my $containSHA256 = 0;
my $debug         = 0;	# 0 for no debugging, 1 for debugging hash digests

getopts( 'd:o:', \%optctl ) or usage();

# required both flags to contain values (-d and -o)
if ( ( defined $optctl{d} ) && ( defined $optctl{o} ) ) {

	my $startdir   = $optctl{d};
	my $outputfile = "$startdir/$optctl{o}";

	# test and see if the directory actually exists
	if ( -d $startdir ) {

		my $tempdir = "$startdir/hashcheck";

		# get all files in directory
		find($startdir);

		# make out tempdir, tempdir is used for unzipping the gzipped files
		# then we do a md5sum/sha256sum on them for verification
		mkdir $tempdir, "0755";

		# start the loop
		foreach $name ( sort @files ) {

			# if its a directory, skip me
			if ( -d $name ) {
				next;
			}

			# or if its a file, lets work on it
			else {
				if ( $name =~ /.gz/ ) {

					# using File::Basename here and parse the file path
					my ( $filename, $directories, $suffix ) =
					  fileparse( $name, @suffixes );

					my $outfile = "$tempdir/$filename";

					# remove .gz from name
					$outfile =~ s/\.gz//g;

					# if we have a .info file, lets take a look at it
					if ($suffix) {

						$counter++;
						print("File[$counter]:\n");

						# string manipulation to get the .gz filename
						$gzipped_file = "$directories$filename";
						$gzipped_file =~ s/\.info//g;
						print("GZfile = $gzipped_file\n");
						print("INFo file = $name\n");

						# call the gunzip subroutine
						gunzip( $gzipped_file, $outfile );

						my $fh = new FileHandle "<$gzipped_file";
						$md5hash = genMD5($fh);
						close($fh);

						$shafh      = new FileHandle "<$gzipped_file";
						$sha256Hash = genSHA256($shafh);
						close($shafh);

						# lets open up the info file now
						open( FH, "<$name" );
						while (<FH>) {
							next if s/#.*//;
							next if /^(\s)*$/;

							@line = split( '=', $_ );

							if (   ( $line[0] =~ /post/ )
								&& ( $line[0] =~ /MD5/ ) )
							{
								$containMD5 = 1;

								if ( $md5hash == $line[1] ) {
									print(
										"MD5 POST-compression check:  VALID\n");

									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:   $md5hash\n\n")
									  if $debug;

								}
								else {
									print(
"MD5 POST-compression check:  NOT-VALID\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:   $md5hash\n\n")
									  if $debug;

								}
							}

							if (   ( $line[0] =~ /precompressed/ )
								&& ( $line[0] =~ /MD5/ ) )
							{
								$containMD5 = 1;
								$fh         = new FileHandle "<$outfile";
								my $md2 = genMD5($fh);
								close($fh);
								if ( $md2 == $line[1] ) {

									print(
										"MD5 PRE-compression check:  VALID\n");
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $md2\n\n")
									  if $debug;
								}
								else {

									print(
"MD5 PRE-compression check:  NOT-VALID\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $md2\n\n")
									  if $debug;

								}

							}

							if (   ( $line[0] =~ /SHA256/ )
								&& ( $line[0] =~ /post/ ) )
							{
								$containSHA256 = 1;

								if ( $sha256Hash == $line[1] ) {
									print(
"SHA256 POST-compression check:  VALID\n\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $sha256Hash\n\n")
									  if $debug;
								}
								else {
									print(
"SHA256 POST-compression check:  NOT-VALID\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $sha256Hash\n\n")
									  if $debug;

								}
							}

							if (   ( $line[0] =~ /precompressed/ )
								&& ( $line[0] =~ /SHA256/ ) )
							{
								$containSHA256 = 1;
								$fh            = new FileHandle "<$outfile";
								my $sha2 = genSHA256($fh);
								close($fh);
								if ( $sha2 == $line[1] ) {
									print(
										"SHA256 PRE-compression check:  VALID\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $sha2\n\n")
									  if $debug;
								}
								else {
									print(
"SHA256 PRE-compression check:  NOT-VALID\n"
									);
									print("$name:  $line[1]") if $debug;
									print("$gzipped_file:  $sha2\n\n")
									  if $debug;    

								}

							}

						}
						close(FH);

					}
					$totalfiles++;
				}
			}
		}
		close(OUT);
		my $end       = gettimeofday;
		my $finaltime = $end - $start;
		$finaltime = sprintf( "%.4f seconds", $finaltime );

		print(
			"Number of total (.info and .gz) files in $startdir:  $totalfiles\n"
		);
		print("Total elapsed time:  $finaltime\n");

	}
	else {
		print("ERROR:  $startdir does not exist.\n");
		usage();
	}

}

else {
	usage();
	croak("Bad argument to --dir\n");

}


sub wanted { push @files, $name; }    # This subroutine is called
                                      # for each file found

# Gets the sha1 checksum, currently not used.
sub genSHA1 {

	my $fh     = shift;
	my $digest = Digest::SHA->new(1);

	#The $io_handle will be read until EOF and its content appended to
	#the message we calculate the digest for.  The return value is the
	#$sha1 object itself.
	$digest->addfile($fh);
	return $digest->hexdigest;
}

# gets the SHA256 checksum
sub genSHA256 {

	my $fh = shift;

	#my $sig = Digest::SHA2::new(256);
	my $digest = Digest::SHA->new(256);

	#The $io_handle will be read until EOF and its content appended to
	#the message we calculate the digest for.  The return value is the
	#$sha1 object itself.

	$digest->addfile($fh);
	return $digest->hexdigest;
}

# gets the MD5 checksum
sub genMD5 {

	my $fh     = shift;
	my $digest = Digest::MD5->new();

	#The $io_handle will be read until EOF and its content appended to
	#the message we calculate the digest for.  The return value is the
	#md5 object itself.
	$digest->addfile($fh);
	return $digest->hexdigest;
}

# gunzip's our .gz file for md5sum/sha256sum verfication
sub gunzip {

	#infile will be gzipped here
	my $infile  = shift;
	my $outfile = shift;

	if ( !$infile || !$outfile ) {
		print "$0 <infile> <outfile>\n";
		exit;
	}

	my $buffer;
	my $gz      = undef;
	my $success = 1;

	if ( !open FH, "> $outfile" ) {
		$success = 0;
		print "Unable to write to '$outfile'\n";
	}
	else {
		binmode FH;

		if ( $gz = gzopen( $infile, "rb" ) ) {
			while ( $gz->gzread($buffer) > 0 ) {
				print FH $buffer;
			}
			if ( $gzerrno != Z_STREAM_END ) {
				$success = 0;
				print "ZLib Error: reading $outfile - $gzerrno: $!\n";
			}
			else {
				$success = 1;
			}
			$gz->gzclose;
		}
		else {
			$success = 0;
			print "ZLib Error: opening $infile - $gzerrno: $!\n";
		}
		close FH;
	}
}

# as always, our trusy help menu
sub usage() {
	print "
Usage:
     validatehash.pl -d <dir> -o <output file> 
     -d : starting directory where all your .gz and .info packet capture files are located.
     -o : output file which will contain your report
     
     Example(s):  perl validatehash.pl --dir /data/logfile
";
	exit();
}

