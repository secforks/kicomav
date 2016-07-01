# -*- coding:utf-8 -*-

"""
Copyright (C) 2013-2014 Nurilab.

Author: Kei Choi(hanul93@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

__revision__ = '$LastChangedRevision: 2 $'
__author__   = 'Kei Choi'
__version__  = '1.0.0.%d' % int( __revision__[21:-2] )
__contact__  = 'hanul93@gmail.com'


import kernel
import re

HTML_KEY_COUNT = 3

#---------------------------------------------------------------------
# KavMain 클래스
# 키콤백신 엔진 모듈임을 나타내는 클래스이다.
# 이 클래스가 없으면 백신 엔진 커널 모듈에서 로딩하지 않는다.
#---------------------------------------------------------------------
class KavMain :
    #-----------------------------------------------------------------
    # init(self, plugins)
    # 백신 엔진 모듈의 초기화 작업을 수행한다.
    #-----------------------------------------------------------------
    def init(self, plugins) : # 백신 모듈 초기화
        # HTML 키워드
        pat = r'<html\b|\bDOCTYPE\b|<head\b|<title\b|<meta\b|\bhref\b|\blink\b|<body\b'
        self.html_p = re.compile(pat, re.I)
        
        # script, iframe 키워드
        pat = '<script.*?>[\d\D]*?</script>|<iframe.*?>[\d\D]*?</iframe>'
        self.scr_p = re.compile(pat, re.I)
        

        return 0

    #-----------------------------------------------------------------
    # uninit(self)
    # 백신 엔진 모듈의 종료화 작업을 수행한다.
    #-----------------------------------------------------------------
    def uninit(self) : # 백신 모듈 종료화
        return 0
    
    #-----------------------------------------------------------------
    # getinfo(self)
    # 백신 엔진 모듈의 주요 정보를 알려준다. (버전, 제작자...)
    #-----------------------------------------------------------------
    def getinfo(self) :
        info = {} # 사전형 변수 선언
        info['author'] = 'Kei Choi' # 제작자
        info['version'] = __version__ # 버전
        info['title'] = 'HTML Engine' # 엔진 설명
        info['kmd_name'] = 'html' # 엔진 파일명
        return info

    #-----------------------------------------------------------------
    # format(self, mmhandle, filename)
    # 포맷 분석기이다.
    #-----------------------------------------------------------------
    def format(self, mmhandle, filename) :
        try :
            fformat = {} # 포맷 정보를 담을 공간

            mm = mmhandle

            s = self.html_p.findall(mm[:4096])
            s = list(set(s))

            if len(s) >= HTML_KEY_COUNT : 
                fformat['keyword'] = s # 포맷 주요 정보 저장

                ret = {}
                ret['ff_html'] = fformat

                return ret
        except :
            pass

        return None
        
    #-----------------------------------------------------------------
    # arclist(self, scan_file_struct, format)
    # 포맷 분석기이다.
    #-----------------------------------------------------------------
    def arclist(self, filename, format) :
        file_scan_list = [] # 검사 대상 정보를 모두 가짐

        try :
            # 미리 분석된 파일 포맷중에 ff_text 포맷이 있는가?
            fformat = format['ff_html']
            
            fp = open(filename, 'rb')
            buf = fp.read()
            fp.close()
            
            s = self.html_p.findall(buf)
            s = list(set(s))
            if len(s) >= HTML_KEY_COUNT : # HTML 키워드가 3개 이상 발견되면 HTML 포맷
                # script와 iframe 리스트를 만든다.
                
                s_count = 1
                i_count = 1
                
                for obj in self.scr_p.finditer(buf) :
                    t1 = obj.group()
                    # t2 = obj.span()
                    
                    if t1.lower().find('<script') != -1 : 
                        file_scan_list.append(['arc_html', 'HTML/Script #%d' % s_count])
                        s_count += 1
                    else :    
                        file_scan_list.append(['arc_html', 'HTML/IFrame #%d' % i_count])
                        i_count += 1
                
                '''
                count = 1
                for obj in self.scr_p.finditer(buf) :
                    # t1 = obj.group()
                    # t2 = obj.span()
                    
                    file_scan_list.append(['arc_html', 'HTML #%d' % count])
                    count += 1
                '''
        except :
            pass

        return file_scan_list

    #-----------------------------------------------------------------
    # unarc(self, scan_file_struct)
    # 주어진 압축된 파일명으로 파일을 해제한다.
    #-----------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, arc_in_name) :
        try :
            if arc_engine_id != 'arc_html' :
                raise SystemError

            fp = open(arc_name, 'rb')
            buf = fp.read()
            fp.close()
            
            s = self.html_p.findall(buf)
            s = list(set(s))
            if len(s) >= HTML_KEY_COUNT : # HTML 키워드가 3개 이상 발견되면 HTML 포맷
                # script와 iframe 리스트를 찾는다.
                
                s_count = 1
                i_count = 1
                
                for obj in self.scr_p.finditer(buf) :
                    t1 = obj.group()
                    t2 = obj.span()
                    
                    k = ''
                    if t1.lower().find('<script') != -1 : 
                        k = 'HTML/Script #%d' % s_count
                        s_count += 1
                    else :    
                        k = 'HTML/IFrame #%d' % i_count
                        i_count += 1
                        
                    if k == arc_in_name :
                        data = buf[t2[0]:t2[1]]
                        return data
                        
                '''
                count = 1
                for obj in self.scr_p.finditer(buf) :
                    # t1 = obj.group()
                    t2 = obj.span()
                    
                    k = 'HTML #%d' % count
                    count += 1
            
                    if k == arc_in_name :
                        data = buf[t2[0]:t2[1]]
                        return data
                '''
        except :
            pass

        return None