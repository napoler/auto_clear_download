#! /usr/bin/env python3

import os
import os.path
import sys
import json
import re
import subprocess
from pprint import pprint


def create_video_filter(orig_file_name):
    # use ffprobe to get the width of the original file
    result = subprocess.run(['ffprobe', '-show_streams', '-select_streams',
                            'v', '-of', 'json', orig_file_name], stdout=subprocess.PIPE)
    # print('result.stdout => %s' % result.stdout)
    file_data = json.loads(result.stdout)
    # print('file_data => %s' % file_data)
    width = file_data['streams'][0]['width']

    # make sure the width is an even number
    if (width % 2):
        width -= width
    if width > 1280:
        scale_width = 1280
    else:
        scale_width = width  # the width of the original file rounded down to be even
    # scale_width = width  # the width of the original file rounded down to
    # keep the same aspect ratio but make sure the height is also and even number
    scale_height = 'trunc(ow/a/2)*2'
    video_filter = '-vf "scale=%s:%s"' % (scale_width, scale_height)
    return video_filter, file_data['streams'][0]


def create_new_file_name(orig_file_name,    ffmpeg_args={
    'ab': 128,  # audio bitrate is 128kbps by default
    'vb': 2048,  # video bitrate is 800K by default
}):
    # check to see if search/replace parameters have been passed
    try:
        if ('file-search' in params.keys() and 'file-replace' in params.keys()):
            s = params['file-search']
            p = re.compile(s)
            print('p => %s' % p.pattern)
            replace = params['file-replace']
            result = re.sub(p, replace, orig_file_name)
            # print("result", result)
            # replace spaces with hyphens
            file_name = result.replace(' ', '-')
        else:
            file_name = orig_file_name
    except:
        pass
    try:
        print("result", result)
        if '.mp4' not in result:
            file_name = file_name.replace(result.split('.')[-1], 'mp4')
            pass
    except:
        fls = orig_file_name.split(".")
        # ".".join(fls[:-1])+"_new.mp4"
        file_name = ".".join(fls[:-1])+"_new.mp4"
        pass
    return file_name


def convert_file(orig_file_name, ffmpeg_args,test=False):
    orig_file_ext = orig_file_name.split('.')[-1]
    print("\n\n\n\n")
    print("Starting to convert %s..." % orig_file_name)
    new_file_name = create_new_file_name(orig_file_name, ffmpeg_args)
    print("new_file_name: %s" % new_file_name)

    # vb = ffmpeg_args['vb']
    # if ffmpeg_args['vb'] > 2048:
    #     vb = 2048
    # else:
    #     # exit()
    #     print("auto end : file: %s vb: %s" %
    #           (orig_file_name, ffmpeg_args['vb']))
    #     return
    #     vb = ffmpeg_args['vb']

    # create the video filter
    video_filter, stream = create_video_filter(orig_file_name)
    print('orig_file stream =>')
    pprint(stream)

    avg_frame_rate_arg = stream['avg_frame_rate'].split("/")
    avg_frame_rate = int(avg_frame_rate_arg[0])/int(avg_frame_rate_arg[1])
    # print("avg_frame_rate", avg_frame_rate)

    # if (int(stream['bit_rate']) <= ffmpeg_args['vb']*1024 or stream['coded_width'] <= 1280) and avg_frame_rate < 30:
    if int(stream['bit_rate']) <= ffmpeg_args['vb']*1024 and avg_frame_rate < 30:
        # print("small file auto end:")
        return False
    if test==True:
        return True

    vb=ffmpeg_args['vb']*0.95
    vb=min(vb,950)
        # create the command to convert the file
    # command = 'ffmpeg -i "%s" %s  -acodec aac -strict -2 -ab %sk -ar 44100 -vcodec h264 -vb %sK  -preset ultrafast  -pix_fmt yuv420p  -crf 23  -maxrate 1M -bufsize 2M  "%s" ' % (
    #     orig_file_name, video_filter, ffmpeg_args['ab'], ffmpeg_args['vb'], new_file_name)
    command = 'ffmpeg -i "%s" %s  -acodec aac -strict -2 -ab %sk -ar 44100 -vcodec h264 -vb %sK  -preset fast  -pix_fmt yuv420p  -crf 25  -maxrate 4M -bufsize 4M -r 23.976 "%s" ' % (
        orig_file_name, video_filter, ffmpeg_args['ab'], vb, new_file_name)
    
    # command = 'ffmpeg -i "%s" %s  -acodec aac -strict -2 -ab %sk -ar 44100  -c:v libx265  -vb %sK  -preset fast  -pix_fmt yuv420p  -crf 30  -maxrate 4M -bufsize 4M -r 23.976 "%s" ' % (
    #     orig_file_name, video_filter, ffmpeg_args['ab'], ffmpeg_args['vb'], new_file_name)

    # command = "time %s" % command
    command = "%s -y" % command
    print('convert command: %s' % command)
    # convert the file
    exit_code = os.system(command)

    # exit()

    if (exit_code == 0):
        # move the original file
        # orig_file_new_name = orig_file_name.replace(
        #     '.%s' % orig_file_ext, '_%s' % orig_file_ext)
        # move_command = 'mv "%s" "%s"' % (orig_file_name, orig_file_new_name)

        # orig_file_new_name = orig_file_name.replace(
        #     '.%s' % orig_file_ext, '_%s' % orig_file_ext)

        move_command = 'rm "%s" && mv "%s" "%s"' % (
            orig_file_name, new_file_name, orig_file_name)
        os.system(move_command)
        print(move_command)
        print("\n")
        print("%s created and original file moved to %s" %
              (new_file_name, orig_file_name))

        _, stream = create_video_filter(orig_file_name)
        print(f"new_file stream => {orig_file_name}")
        pprint(stream)
    else:
        os.system('rm "%s"' % (new_file_name))
        print("Converting %s failed, please try again." % orig_file_name)
    pass


def output_help():
    data = {
        'script-name': sys.argv[0].split('/')[-1],  # script name
        'slash_one':   '%s%s' % ('\\', '1'),
    }

    print("""
  Video Converter

  Usage:
      Single file
        %(script-name)s {options} file_name.avi
      Batch processing of files
        %(script-name)s {options} *.avi

      Batch processing of files with regex name replacement - example
        %(script-name)s *.avi --file-search='Castle\.2009\.(.*)\.HDTV.XviD-LOL.*' --file-replace='Castle-(2009).%(slash_one)s.mp4'

  Options:
        -ab=128           Set ffmpeg audio bitrate (128)kbps
        -vb=800           Set ffmpeg video bitrate (800)kbps

        --file-search     Regular Epression Pattern for file name change - remember case counts
        --file-replace    replacement pattern for file name change - for groupings use %(slash_one)s instead of $1
        --test-replace    returns a list of the potential file names from the --file-replace argument
  """ % data)

    return


def simulate_file_name_replace(files_to_convert):
    for file_to_convert in files_to_convert:
        print("%s => %s" % (file_to_convert, create_new_file_name(file_to_convert)))
    pass


if __name__ == "__main__":
    ffmpeg_args = {
        'ab': 128,  # audio bitrate is 128kbps by default
        'vb': 2048,  # video bitrate is 800K by default
    }
    params = {}
    args = sys.argv[1:]
    files_to_convert = []
    for arg in args:
        if ('--' in arg):
            param_name = arg.split('--')[1].split('=')[0]
            if (param_name == 'help'):
                output_help()
                exit()
            if (len(arg.split('=')) > 1):
                param = arg.split('=')[1]
            else:
                param = 1

            params[param_name] = param

        elif (arg[0] == '-'):
            # this is an argument not a file to convert

            ffmpeg_args[arg.split('-')[1].split('=')[0]] = arg.split('=')[1]
        elif (os.path.isfile(arg)):
            # we have confirmed that the argument is a file

            files_to_convert.append(arg)
    print("ffmpeg_args: %s" % ffmpeg_args)

    if ('test-replace' in params.keys()):
        simulate_file_name_replace(files_to_convert)
        exit()

    for file_to_convert in files_to_convert:
        convert_file(file_to_convert, ffmpeg_args)
