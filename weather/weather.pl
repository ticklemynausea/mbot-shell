use Weather::Underground;
use strict;
use warnings;
use utf8;
binmode(STDOUT, ":utf8");
if ($#ARGV == -1) {
  print "Usage: !weather <location>. Try: 'City', 'City, State', 'State', 'State, Country' and 'Country'.\n";
  exit(-1);
}

my $place = join(" ", @ARGV);

my $weather = Weather::Underground->new(
  place => $place,
  debug => 0,
) || print "Error: $@\n";

my $arrayref = $weather->get_weather() || die "Error: $@\n";

foreach (@$arrayref) {
  my $response = "Weather in $_->{'place'}: ";
  my $d;
  my $e;
  my $f;

  $d = $_->{"celsius"};
  if ($d ne "") {
    $response .= "$d"."ºC";
  }

  $d = $_->{"conditions"};
  if ($d ne "") {
    $response .= "/$d; ";
  } else {
    $response .= "; ";
  }
  
  $d = $_->{"wind_direction"};
  if ($d ne "") {
    $response .= "Wind: $d";
  }
  
  $d = $_->{"wind_kilometersperhour"};
  if ($d ne "") {
    $response .= "/$d Km/h; ";
  } else {
    $response .= "; ";
  }
  
  $d = $_->{"pressure"};
  if ($d ne "") {
    $response .= "Pressure: $d; ";
  }
  
  $d = $_->{"humidity"};
  if ($d ne "") {
    $response .= "Humidity: $d%; ";
  }

  $d = $_->{"sunrise"};
  $e = $_->{"sunset"};
  if ($d ne "") {
    $d = substr($d, 0, -4);
    $e = substr($e, 0, -4);
    $response .= "Sunrise/Sunset: $d/$e; ";
  }

  $d = $_->{"moonphase"};
  $e = $_->{"moonrise"};
  $f = $_->{"moonset"};
  if ($d ne "") {
    $e = substr($e, 0, -4);
    $f = substr($f, 0, -4);
    $response .= "Moon Rise/Set: $d $e/$f; ";
  }

  #  while (my ($key, $value) = each %{$_}) {
  #    if (defined $value) {
  #        print "\t$key = $value\n";
  #      } else {
  #        print "\t$key = ?\n";
  #      }
  #  }

  print $response."\n";
}




