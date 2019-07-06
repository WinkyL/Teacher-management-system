from django.db import models

# Create your models here.

class Teacher(models.Model):
    SEX_CHOICES = (
        (0, '男'),
        (1, '女'),
    )
    COL_CHOICES = (
        (0, '中俄学院'),
        (1, '哲学学院'),
        (2, '政府管理学院'),
        (3, '经济与工商管理院'),
        (4, '法学院'),
        (5, '教育科学研究学院'),
        (6, '文学院'),
        (7, '新闻传播学院'),
        (8, '西语学院'),
        (9, '俄语学院'),
        (10, '东语学院'),
        (11, '艺术学院'),
        (12, '历史文化旅游学院'),
        (13, '数学科学学院'),
        (14, '物理科学与技术学院'),
        (15, '化学化工与材料学院'),
        (16, '生命科学学院'),
        (17, '机电工程学院'),
        (18, '电子工程学院'),
        (19, '计算机科学技术学院'),
        (20, '软件学院'),
        (21, '信息科学与技术学院'),
        (22, '建筑工程学院'),
        (23, '水利电力学院'),
        (24, '农作物研究院'),
        (25, '农业资源与环境学院'),
        (26, '信息管理学院'),
        (27, '应用外语学院'),
        (28, '俄语语言文学中心'),
        (29, '马克思主义学院'),
        (30, '国际文化教育学院'),
        (31, '满族语言文化研究中心')
    )
    TIT_CHOICES = (
        (0, '教授'),
        (1, '副教授'),
        (2, '讲师'),
        (3, '助理讲师'),
    )
    EDU_CHOICES = (
        (0,'专科'),
        (1,'本科'),
        (2,'硕士'),
        (3,'博士'),
        (4,'博士后'),
    )
    CHE_CHOICES = (
        (0, '待审核'),
        (1, '已审核'),
        (2, '审核未通过')
    )
    RAT_CHOICES = (
        (0, '未填写课时'),
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, '待评级'),
    )
    work_ID = models.IntegerField('WorkID', primary_key= True)
    name = models.CharField('Name', max_length=10)
    email = models.EmailField('Email', null= True)
    sex = models.IntegerField('Sex', choices=SEX_CHOICES,default=0)
    card_ID = models.CharField('CardID', max_length=18,default='')
    age = models.PositiveIntegerField('age',default=0)
    address = models.CharField('Addre', max_length=100,default='')
    nation = models.CharField('Nation', max_length=40, default='')
    birthplace = models.CharField('BirthPlace', max_length=100, default='')
    phonenum = models.CharField('Phone', max_length=15, default='')
    title = models.IntegerField('Title', choices=TIT_CHOICES, default= 2)
    firstedu = models.IntegerField('FirstEdu', choices=EDU_CHOICES, default=1)
    firstsch = models.CharField('FirstSch', max_length=100, default='')
    finaledu = models.IntegerField('FinalEdu', choices=EDU_CHOICES, default=1)
    finalsch = models.CharField('FinalSch', max_length=100, default='')
    honor = models.TextField('Honor', default='')
    college = models.IntegerField('College', choices=COL_CHOICES,default=0)
    entry_time = models.DateField('EntryTime',default='')
    checkstatus = models.IntegerField('CheckStu', choices=CHE_CHOICES, default=0)
    last5 = models.IntegerField('Last5', default=0)
    last4 = models.IntegerField('Last4', default=0)
    last3 = models.IntegerField('Last3', default=0)
    last2 = models.IntegerField('Last2', default=0)
    last1 = models.IntegerField('Last1', default=0)
    rate = models.IntegerField('Rate', choices=RAT_CHOICES,default=0)

    def __str__(self):
        return self.work_ID

    class Meta:
        ordering = ['name']


class User(models.Model):
    STATUS_CHOICE = (
        (0, 'admin'),
        (1, 'teacher'),
    )
    username = models.OneToOneField('Teacher', primary_key= True, on_delete=models.CASCADE)
    password = models.CharField(max_length=15)
    status = models.IntegerField(choices=STATUS_CHOICE)

    def __str__(self):
        return self.username

#class Photo(models.Model):
#    username = models.OneToOneField('Teacher', primary_key=True, on_delete=models.CASCADE)
#    img = models.ImageField(upload_to='img', default='img/0.jpg')
#    def __str__(self):
#        return self.username

