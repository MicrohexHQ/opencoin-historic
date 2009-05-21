import UserDict, cPickle, blowfish, random, os, base64
class Storage(UserDict.UserDict):

    def setFilename(self,filename):
        self.filename = filename
        return self

    def save(self):
        cPickle.dump(self.data,open(self.filename,'w'))
        return self

    def restore(self):
        try:
            self.data = cPickle.load(open(self.filename))
        except:            
            pass
        return self

class CryptedStorage(Storage):

    prefix = 'salt'

    def setPassword(self,password):
        self.password = password


    def decrypt(self,password,salt,text):
        key = str(password+salt)
        cipher = blowfish.Blowfish(key)
        cipher.initCTR()
        return cipher.decryptCTR(text)

    def encrypt(self,password,salt,text):       
        key = str(password+salt)
        cipher = blowfish.Blowfish(key)
        cipher.initCTR()
        return cipher.encryptCTR(text)


    def save(self):
        data = 'opencoin'+base64.b64encode(cPickle.dumps(self.data))
        salt = ''.join([str(random.randint(0,9)) for i in range(0,16)])
        crypted = self.encrypt(self.password,salt,data)
        content = '%s%s%s' % (self.prefix,salt,base64.b64encode(crypted))
        open(self.filename,'w').write(content)
        return self


    def restore(self):
        if os.path.exists(self.filename):
            content = open(self.filename).read()
            if content.startswith(self.prefix):
                salt = content[4:20]
                crypted = base64.b64decode(content[20:])
                data = self.decrypt(self.password, salt, crypted)
                if data.startswith('opencoin'):
                    data = data[8:]
                else:
                    raise 'wrong password'
                data = base64.b64decode(data)                    
            else:
                data = content
            
            self.data = cPickle.loads(data)
        return self            
                            


    
