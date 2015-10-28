#-*- encoding: utf-8 -*-
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

chosung_list = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ" ]
jungsung_list = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅛ","ㅙ","ㅚ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
jongsung_list = [" ","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

#0 1 2 3 4 5 6 7 8 9
digit_list = [True, True, False, True, False, False, True, True, True, False]

#a b c d e f g h i j k l m n o p q r s t u v w x y z
alphabet_list = [False, True, True, True, False, False, False, False, False, False, True, True, True, True, False, True, True, False, False, True, False, False, False, False, False, False]
alphabet_alone_list = [False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, True, False, False, False, False, False, False, False, False]



def make_sentence(frame,condition):
    #### 조사 처리
    i=0
    position=[]
    for m in re.finditer('post', frame):
        i=i+1
        position.append([m.start(), m.end()])
    
    if i>0:
        frame_copy=frame
        num=len(condition)
        posts=[]
        for pos in position:
            p=pos[0]
            if frame_copy[p-3]=="%":p=p-6
            index=int(find_number(frame_copy,p-2))
            post="이" if has_jongsung(condition[index]) else "가"
            posts.append(post)
            frame=str(frame.replace("post",str(num),1))
            num+=1            
        
        for pos in posts:
            condition.append(pos)
            
        sentence=frame.format(*condition)        
    else:
        sentence=frame.format(*condition)

    return sentence

def find_number(s,p):
    start=0
    end=0
    i=0
    num=''
    while True:
        if is_number(s[p-i]):
            num+=s[p-i]
        else:
            if s[p-i]=="{": return num[::-1]
        i=i+1

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False  
    

def has_jongsung(word):
	#공백일 경우 처리
	if word == "":
		return True

	last_char = unicode(word)[-1].upper()
	uni = ord(last_char)
	
	offset = ord(u'0')
	if uni >= offset and uni < offset + 10:
		# print (uni-offset)
		return digit_list[ (uni-offset) ]

	offset = ord(u'A')
	if uni >= offset and uni < offset + 26:
		if len(word) == 1 or word[-2] == ' ' or word[-2] == '.':
			return alphabet_alone_list[ (uni-offset) ]
		else:
			if last_char == u'E':
				last_char = unicode(word)[-2].upper()
				uni = ord(last_char)
			return alphabet_list[ (uni-offset) ]

	offset = ord(u"가")
	jongsung = jongsung_list[ (uni-offset) % len(jongsung_list) ]
	if jongsung == " ":
		return False
	else:
		return True    