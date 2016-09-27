import cherrypy
import random
import string

#
# Survey engine in CherryPy
# Python 2.*
#
class SurveyThing:
    _cp_config = {'tools.sessions.on': True}
    
    def index(self):
        # get or create generator
        ig = cherrypy.session.get('ig', self.instrument())
        
        # iterate once
        qtext = ig.next()
        
        # save generator
        cherrypy.session['ig'] = ig
        
        # return value
        return qtext
    index.exposed = True
    

    def mq(self, question, choices, randomize=True):
        form = '<form action="hq" method="GET">  %s<br/>' % question
        if randomize:
            choices = list(choices)
            random.shuffle(choices)  
        for x in choices:
            form = form + '<input type="radio" name="var" value="%s"/>%s<br/>' % (x[1],x[0])
        form = form + '<input type="submit"/></form>'
        return form
    
    
    def hq(self, var):
        survey = cherrypy.session.get('survey',{})
        survey[var] = 1
        cherrypy.session['survey'] = survey   #<<<< probably could tie in as class variable
        return '''So far: %s.<br/>[<a href='./index'>NEXT</a>]''' % survey.keys()
    hq.exposed = True

    
    def score(self):
        pass

    
    def instrument(self):
        for q in self.questions:
            yield self.mq(q[0],*q[1:])
        s = self.score()
        yield 'Your worldview:<br/>%s' % s
    
    
    def addq(self, question, *rcs):
        self.questions.append((question,rcs))
    
        
    def ci(self):
        pass
        #varnames = []
        #for q in self.questions:
        #    for rc in q[1]:
        #        varnames.append(rc[1])
        #varnames.sort()
        #print 'hey matt'
    


#
# Sample survey: Religious worldview
# Text not mine
#
class SurveyThingJR(SurveyThing):
    def __init__(self):
        self.questions = []
        self.mi()
    
    
    def score(self):
        survey = cherrypy.session.get('survey')     
        atheism_score, pantheism_score, pan_en_theism_score, deism_score, finite_godism_score, monotheism_score, polytheism_score, biblical_christianity_score = 0,0,0,0,0,0,0,0
        for x in ('nogod','physicalreality','realfromunknown','humanfromevolution','humansgoodorbadcancorrect','knowsensesdeduction','rightwrongexperiencereason','truthultimateexplanation','evildestructive','lawsfromhumans','deathceaseexist','miraclesno','historynomeaning','knownogod'):
            atheism_score = atheism_score + survey.get(x,0)
        for x in ('godisall','godrealworldillusion','onlygodreal','humanessencegod','humansgoodplusillusion','knowgodhoodonly','rightwrongillusion','truthillusion','evilillusion','lawsillusion','deathreincarnation','deathreincarnation','miraclesyesillusory','historyillusion','knowgodwithin'):
            pantheism_score = pantheism_score + survey.get(x,0)
        for x in ('godisinall','godrealgeneratesreality','realfromgod','humanpartofgod','humansgoodandbad','knowbygrow','rightwronggrowth','truththroughgrowth','evilmistakes','lawsevergrowinggod','deathmaybeafterlife','miraclesno','knowgodcosmos'):
            pan_en_theism_score = pan_en_theism_score + survey.get(x,0)
        for x in ('distantcreator','godmakerofreal','realfromgod','humanmostcomplex','humansgoodorbadchoice','knowsensesdeduction','truthmindofgod','evilirrational','lawsreflectmindgod','deathmaybeafterlife','miraclesno','historystorymankind','knowgodthroughcreation'):
            deism_score = deism_score + survey.get(x,0)
        for x in ('limitedgod','godandothereternalarereal','realfromgodandother','humancreatedortheisticallyevolved','humansgoodorbad','knowreasonrevelation','rightwrongrevelation','truthgodoperates','evilgodsenemy','lawsmadebygod','deathrewardpunishment','miraclesyesintheory','historystugglegoodevil','knowgodally'):
            finite_godism_score = finite_godism_score + survey.get(x,0)
        for x in ('manygods','godsandcosmosreal','realfromvarious','humancreationofgods','humansgoodorbad','rightwrongexperiencereason','knowreasonrevelation','rightwrongrevelation','truthultimatereality','evildisharmony','lawsdecisionsgods','deathplaceofdead','historyentertainmentgods','knowgodseach'):
            polytheism_score = polytheism_score + survey.get(x,0)
        for x in ('onegod','godmakerofreal','realfromgodfromnothing','humansignaturemasterpiece','humansbentcanovercome','miraclesyes','knowbeginswithworship','rightwrongactingrevelation','truthgodbasis','evilgodisnot','lawsgodreveals','historyglorygod','knowgodonly'):
            monotheism_score = monotheism_score + survey.get(x,0)
        for x in ('onetriunegod','godmakerofreal','realfromgodfromnothing','humansignaturemasterpiece','humansbentonlygodcanfix','deathheavenhell','miraclesyes','knowbeginswithworship','rightwrongactingrevelation','truthgodbasis','evilgodisnot','lawsgodreveals','lawsgodreveals','deathheavenhell','miraclesyes','historyglorygod','knowjesus'):
            biblical_christianity_score = biblical_christianity_score + survey.get(x,0)
            
        all = {'ATHEIST':atheism_score, 'PANTHEIST':pantheism_score, 'PAN-EN-THEIST':pan_en_theism_score,
               'DEIST':deism_score, 'FINITE GOD-IST':finite_godism_score, 'POLYTHEIST':polytheism_score,
               'MONOTHEIST':monotheism_score, 'BIBLICAL CHRISTIAN':biblical_christianity_score}
        rev = {}
        for x in all.keys():
            try:
                rev[all[x]].append(x)
            except KeyError:
                rev[all[x]] = [x]
        
        k = rev.keys()
        k.sort()
        k.reverse()
        r = []
        for x in k:
            r.append((x,rev[x]))
            
        subjective = {8:'Perfectly', 7:'Extremely', 6:'Very', 5:'More than Moderately', 4:'Moderately', 3:'Somewhat', 2:'More than a little', 1:'A little', 0:'Not at all'}
        sout = ''
        for x in r:
            sout = sout + '%s %s <br/>' % (subjective[x[0]], string.join(x[1],', '))
            
        return str(sout)
        
            

    
    def mi(self):
        self.addq(
                    'Is there a God?',
                    ('There is no God','nogod'),
                    ('God is all','godisall'),
                    ('God is <em>in</em> all','godisinall'),
                    ('God is a distant Creator','distantcreator'),
                    ('There is a God, but He is limited','limitedgod'),
                    ('There are many Gods','manygods'),
                    ('There is only one God','onegod'),
                    ('There is only one Triune God','onetriunegod'))
        
        self.addq(
                    'What is real?',
                    ('Physical matter and energy are the only reality','physicalreality'),
                    ('God is real, but the world is an illusion','godrealworldillusion'),
                    ('God is real and generates reality','godrealgeneratesreality'),
                    ('God is the maker of the real','godmakerofreal'),
                    ('God and something else are real','godandothereternalarereal'),
                    ('Gods and the cosmos are real','godsandcosmosreal'))
        
        self.addq(
                    "Where did What's Real come from?",
                    ('Unknown','realfromunknown'),
                    ('Only God is real','onlygodreal'),
                    ('God','realfromgod'),
                    ('God and something else','realfromgodandother'),
                    ('Various theories (myths) about origins','realfromvarious'),
                    ('God who created out of nothing','realfromgodfromnothing'))
        
        self.addq(
                    'What is a human being?',
                    ('Humans are a product of evolution','humanfromevolution'),
                    ('The human core is the same essence as God','humanessencegod'),
                    ('Part of God','humanpartofgod'),
                    ("Most complex creature of God's making",'humanmostcomplex'),
                    ('Produced by God (possible for humans to be either created or theistically evolved','humancreatedortheisticallyevolved'),
                    ('Creation of the gods','humancreationofgods'),
                    ('Created from God and his signature masterpiece','humansignaturemasterpiece'))
        
        self.addq(
                    'Are humans basically good or evil?  How bad is the flaw?',
                    ('People can be either good or bad; humans may be flawed but can be corrected','humansgoodorbadcancorrect'),
                    ('Humans are good internally but may be caught in outward illusion; the flaw is also illusion','humansgoodplusillusion'),
                    ('Humans are both; flaw is part of the growth process','humansgoodandbad'),
                    ('People can be either good or bad--they contain all that is necessary for choosing; no flaw exists','humansgoodorbadchoice'),
                    ('Can be either; no flaw exists','humansgoodorbad'),
                    ("Originally good, but now bent; the flaw is serious but can be overcome with God's help",'humansbentcanovercome'),
                    ('Originally good, but now bent; the flaw is fatal, and only God can fix it', 'humansbentonlygodcanfix'))
        
        self.addq(
                    'Is it possible to know anything at all?',
                    ('Yes, but only by the senses and logical deduction','knowsensesdeduction'),
                    ('Only recognition of godhood is real, all else is illusion','knowgodhoodonly'),
                    ('Yes, by the experience of becoming/growing','knowbygrow'),
                    ('Yes, by reason and supernatural revelation','knowreasonrevelation'), 
                    ('The worship of God is the beginning of all knowledge','knowbeginswithworship'))  
        
        self.addq(
                    'How do we know what is right and wrong?',
                    ('By experience and reason','rightwrongexperiencereason'),
                    ('Right and wrong are illusion','rightwrongillusion'),
                    ('By growth and becoming','rightwronggrowth'),
                    ('By reason and supernatural revelation','rightwrongrevelation'),  
                    ("By God's acting on the reason, and supernatural revelation",'rightwrongactingrevelation'))  
        
        self.addq(
                    'What is truth?',
                    ('Truth is the ultimate explanation','truthultimateexplanation'),
                    ('Truth is an illusion','truthillusion'),
                    ('Truth is that which God realizes, or makes real, through growth','truththroughgrowth'),
                    ('Truth is the mind of God','truthmindofgod'),
                    ('Truth is that by which God operates','truthgodoperates'),
                    ('Truth is ultimate reality','truthultimatereality'),  
                    ('God is the basis for all truth','truthgodbasis'))  
        
        self.addq(
                    'What is evil?',
                    ('Evil is that which is destructive','evildestructive'),
                    ('Evil is an illusion','evilillusion'),
                    ('Evil is simply mistakes to be overcome','evilmistakes'),
                    ('Evil that which is irrational','evilirrational'),
                    ("Evil is God's enemy",'evilgodsenemy'),
                    ('Evil is disharmony, imbalance','evildisharmony'),   
                    ('Evil is what God is not and does not do','evilgodisnot'))  
        
        self.addq(
                    'Where do laws come from?',
                    ('Humans make laws','lawsfromhumans'),
                    ('Laws are a part of this world of illusion','lawsillusion'),
                    ('Laws evolve out of the evergrowing mindof God','lawsevergrowinggod'),
                    ("Laws reflect God's mind and are built into Creation",'lawsreflectmindgod'),
                    ('Laws are made by God','lawsmadebygod'),
                    ('Laws are the decisions of the gods','lawsdecisionsgods'),
                    ('Laws are built into Creation and God reveals them','lawsgodreveals'))  
        
        self.addq(
                    'What happens to a person at death?',
                    ('Ceases to exist','deathceaseexist'),
                    ('Reincarnation or absorption into God','deathreincarnation'),
                    ('There may be some afterlife','deathmaybeafterlife'),
                    ('Some kind of afterlife of reward or punishment','deathrewardpunishment'),
                    ('Soul goes to place of the dead, may be immortalized','deathplaceofdead'),
                    ('Judgment and either heaven or hell','deathheavenhell'))  
        
        self.addq(
                    'Can miracles happen?',
                    ('Yes, but they are illusory','miraclesyesillusory'),
                    ('No','miraclesno'),
                    ('Yes in theory, but most systems say no in practice','miraclesyesintheory'),
                    ('Yes','miraclesyes'))
        
        self.addq(
                    'What is the meaning of human history?',
                    ('There is no ultimate meaning','historynomeaning'),
                    ('History and its meaning are both illusion','historyillusion'),
                    ('History is part of the unfolding of God','historyunfoldinggod'),
                    ('History is the self-created story of humankind','historystorymankind'),
                    ('History struggle between good and evil','historystugglegoodevil'),
                    ('History is entertainment for the gods','historyentertainmentgods'),
                    ('History is the drama God has created for His glory and for human good','historyglorygod'))  
        
        self.addq(
                    'How do we get to know God?',
                    ('There is no God to know','knownogod'),
                    ('Look within; god is in person','knowgodwithin'),
                    ('By knowing the evolving spirit of the cosmos','knowgodcosmos'),
                    ("By examining God's creation",'knowgodthroughcreation'),
                    ("By allying ourselves to God and God's cause",'knowgodally'),
                    ("By reverencing each deity's worship system",'knowgodseach'),
                    ('By worshipping and following God only','knowgodonly'),   
                    ('Only through relationship with Christ that involves believing and following Him','knowjesus'))
        
        self.ci()


cherrypy.tree.mount(SurveyThingJR())


if __name__ == '__main__':
    import os.path
    thisdir = os.path.dirname(__file__)
    cherrypy.quickstart()
