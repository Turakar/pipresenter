# PiPresenter - Turning your Raspberry Pi into a presenter!
# Copyright (C) {2017}  {Tilman Hoffbauer}
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>. 


import json
import urllib
import urllib.request
import os
import errno

base_url = "https://tfgym-duesseldorf.lms.schulon.org"
token_url = "/login/token.php?username=%s&password=%s&service=moodle_mobile_app"
wsfunction_url = "/webservice/rest/server.php?wstoken=%s&wsfunction=%s&moodlewsrestformat=json"
download_folder = "/tmp/moodledownload/"

token = None
userid = None
files = None

def connect(username, password):
    global token, userid, files
    
    token = None
    userid = None
    files = None
    
    token_req = urllib.request.Request(base_url + token_url % (urllib.parse.quote(username, safe=""), 
                                                                urllib.parse.quote(password, safe="")))
    with urllib.request.urlopen(token_req) as response:
        result = json.loads(response.readall().decode("utf-8"))
        if "errorcode" in result:
            raise Exception(result["errorcode"])
        token = result["token"]
    
    siteinfo = call_wsfunction("moodle_webservice_get_siteinfo")
    userid = siteinfo["userid"]
    
    try:
        os.makedirs(download_folder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(download_folder):
            pass
        else:
            raise


def call_wsfunction(function, **params):
    url = base_url + wsfunction_url % (token, function)
    for k, v in params.items():
        url += "&" + k + "=" + str(v)
    
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.readall().decode("utf-8"))
        return result


def list():
    global files
    if files == None:
        files = call_wsfunction("core_files_get_files", contextid=-1, contextlevel="user", instanceid=userid, 
                                component="user", filearea="private", itemid=0, filepath="", filename="")["files"]
    
    l = []
    for f in files:
        l.append(f["filename"])
    return l


def download(filename):
    if "/" in filename:
        return
    for f in files:
        if f["filename"] == filename:
            url = f["url"]
            if not "webservice" in url:
                url = url.replace("/pluginfile", "/webservice/pluginfile")
            url += "?token=" + token
            path = download_folder + filename
            urllib.request.urlretrieve(url, path)
            return path
