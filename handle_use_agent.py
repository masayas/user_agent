# -*- coding: utf-8 -*-
import re
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time


UA_DEFINITIONS = [
    # imodeブラウザ2.0からのアクセスの場合はフラグを立てる
    # (例: DoCoMo/2.0 N901iS(c100;TB;W24H12) )
    r'DoCoMo\/2\.0',

    # Softbank携帯からのアクセスの場合はフラグを立てる
    # (例: SoftBank/1.0/910T/TJ001/SN123456789012345
    # Browser/NetFront/3.3 Profile/MIDP-2.0 Configuration/CLDC-1.1)
    r'SoftBank',

    # Vodafone携帯からのアクセスの場合はフラグを立てる
    # (例: Vodafone/1.0/V802SE/SEJ001[/▲▲▲▲]
    # Browser/VF-Browser/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1)
    r'Vodafone',

    # au携帯からのアクセスの場合はフラグを立てる
    # （例：KDDI-HI31 UP.Browser/6.2.0.5 (GUI) MMP/2.0）
    r'KDDI-[\w\W]*UP.Browser',

    # willcom携帯からのアクセスの場合はフラグを立てる
    # （例: Mozilla/3.0(WILLCOM;KYOCERA/402KC/2;[FW_ver]/1/C256) NetFront/3.4)
    r'WILLCOM',

    # emobile携帯からのアクセスの場合はフラグを立てる
    # 例: emobile/1.0.0 (H11T; like Gecko; Wireless) NetFront/3.4)
    r'emobile',

    r'iPhone',

    r'iPad',

    # Linux or Unix-like system
    r'X11',

    r'Android',

    r'Nintendo DSi',

    r'Windows',

    r'Macintosh'
]


def count_user_agents():
    """
    Count User Agents
    """
    lines = open("user_agent_history.log", "r")

    # create a list that holds count of user agents plus unknown
    ua_number_list = [0 for _ in range(len(UA_DEFINITIONS)+1)]
    unknown_agent_list = list()
    for line in lines:
        for ua_number, ua_string in enumerate(UA_DEFINITIONS):
            if re.search(ua_string, line):
                ua_number_list[ua_number] += 1
                break
            # if the user agent in the log does not match any of the USER
            # Definitions, save that into a list (unknown_agent_list)
            # and also count it as unknown
            if ua_number == len(UA_DEFINITIONS)-1:
                ua_number_list[len(UA_DEFINITIONS)] += 1
                unknown_agent_list.append(line)

    # print relevant number as an output
    print('total count: {}'.format(sum(ua_number_list)))
    print(ua_number_list)
    print('Unknown Agent: {}'.format(unknown_agent_list))

    return ua_number_list


def find_times():
    """Based on the log, find the min and max time"""
    lines = open("user_agent_history.log", "r")

    for idx, line in enumerate(lines):
        if idx == 0:
            # pick a string from the first line
            # and convert the first 19th string to
            # 'yyyy-mm-dd hh:mm:ss'
            min_time = time.strftime(line[:19])
        pass
    # from the last line, convert to
    # 'yyyy-mm-dd hh:mm:ss'
    max_time = time.strftime(line[:19])
    return min_time, max_time


def plot_access(ua_number_list, min_time, max_time):

    N = len(ua_number_list)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.8       # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind+width/2.0, ua_number_list, width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Access')
    ax.set_title('User Agent (total count={})\n from {} to {}'.format(sum(ua_number_list), min_time, max_time))
    ax.set_xticks(ind + width)
    xlabel = UA_DEFINITIONS+['unknown']
    xlabel[3]= 'au'
    xlabel[0]= 'Docomo'
    xlabel[8]= 'Linux'
    ax.set_xticklabels(tuple(xlabel))
    ax.set_ylim([0, max(ua_number_list)+ 100])

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    plt.show()

if __name__ == "__main__":

    # count the number of user agents
    user_agent_list = count_user_agents()

    min_time, max_time = find_times()

    # based on the number, plot it
    plot_access(user_agent_list, min_time, max_time)
