# web自动化：pytest-bdd + playwright + allure


## 目录结构
```
├── config
    └── env_config.py                  //环境配置
    └── global_vars.py                 //全局变量
    └── path_config.py                 //路径配置
    └── run_config.py                 //运行配置
├── lib                                //第三方库
├── logs                               //日志
├── report                             //测试报告
├── pages                             //页面操作封装
    └── common_page.py                //基础页面
    └── login_page.py                 //登录页面
    ├── bms                           //统一平台页面
    ├── ...                         
├── testcases                         //测试用例
    ├── features                      //场景用例
    ├── step_defs                     //步骤函数
    └── conftest.py 
├── utils                             //工具类方法
    ├── base_utils                      //基础函数封装
    ├── data_utils                      //数据处理
    ├── log_utils                       //日志处理
    ├── report_utils                   //报告处理
    ├── ui_utils                      //playwright基础操作封装
└── conftest.py                
└── pytest.ini
└── README.md
└── execute.py                       //程序入口
```

## 用例编写的一些标准
1. 尽量都使用css或xpath进行定位