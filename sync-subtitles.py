#!/usr/bin/python3

import argparse
import re
from datetime import timedelta

parser = argparse.ArgumentParser(description="Syncing subtitles by shifting the subtitles up or down by some milliseconds")
parser.add_argument('--forward', type=int, help='Milliseconds to move all timestamps forward')
parser.add_argument('--backward', type=int, help='Milliseconds to move all timestamps backwards')
parser.add_argument('inputFile', type=str, help='SRT file to shift the timestamps for')
parser.add_argument('outputFile', type=str, help='SRT file to produce with the shifted timestamps')

args = parser.parse_args()

forward_millis = args.forward if args.forward is not None else 0
backward_millis = args.backward if args.backward is not None else 0

millis_offset = forward_millis - backward_millis

offset_time_delta = timedelta(milliseconds=millis_offset)

input_file = args.inputFile
output_file = args.outputFile

output_file_lines = []

timestamp_regex = re.compile('[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}')

def get_timestamps(line):
  timestamps = re.findall(timestamp_regex, line)
  return timestamps

def delta_to_timestamp_str(time_delta):
  
  hours = time_delta.seconds // 3600
  minutes = time_delta.seconds // 60 - hours * 60
  seconds = time_delta.seconds - hours * 3600 - minutes * 60
  millis = time_delta.microseconds // 1000

  return "{:02}:{:02}:{:02},{:03}".format(hours, minutes, seconds, millis)

def increment_timestamps(timestamps, offset):
  output_timestamps = []

  for timestamp in timestamps:
    time_elements = timestamp.split(':')
    hours = int(time_elements[0])
    minutes = int(time_elements[1])
    seconds, milliseconds = [int(str_num) for str_num in time_elements[2].split(',')]
    time_delta = timedelta(hours=hours,minutes=minutes,seconds=seconds, milliseconds=milliseconds)
    new_time_delta = time_delta + offset_time_delta
    output_timestamps.append(delta_to_timestamp_str(new_time_delta))
  return output_timestamps
    

with open(input_file, 'r') as opened_file:
  for line in opened_file:
    timestamps = get_timestamps(line)        

    if len(timestamps) == 0:
      output_file_lines.append(line)
    else:
      new_timestamps = increment_timestamps(timestamps, offset_time_delta)
      output_file_lines.append(" --> ".join(new_timestamps) + "\n")

with open(output_file, 'w') as file_to_write:
  for output_file_line in output_file_lines:
    file_to_write.write(output_file_line)  
