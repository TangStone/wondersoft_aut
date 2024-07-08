[toc]

# 接口+ui自动化框架:python+pytest+request+pytest-bdd+playwright+yaml+allure

## 目录结构
```
├── ApiData                           // 接口基本信息及测试数据（各个接口用例之间不存在调用情况）
    ├── bms                         
    ├── ...                    
├── common                           // 公共方法
    └── allure_handle.py             //报告处理
    └── base_page.py                 //ui基础组件方法
    └── basefunc.py                  //基础方法
    └── checkresult.py               //断言
    └── customscript.py              //执行自定义脚本
    └── data_handle.py               //ui数据处理 
    └── database.py                  //数据库操作
    └── encryption.py                //加密
    └── exceptions_handle.py         //异常处理
    └── extract.py                   //处理参数传递
    └── handleallure.py              //allure处理
    └── handledict.py                //字典处理
    └── handleyaml.py                //yaml文件处理
    └── logger_handle.py              //日志处理
    └── readcase.py                  //处理用例数据
    └── regroupdata.py               //用例重组
    └── relevancecase.py             //关联用例处理
    └── runcase.py                   //执行用例
    └── sendemail.py                 //发送邮件
    └── teardowncase.py              //后置用例处理
├── config                          // 配置
    └── __init__.py               
    └── env_config.yml              //基础环境配置
    └── global_vars.yaml            //全局变量
    └── path_config.py              //路径配置
    └── run_config.py               //运行配置
├── data                           // ui用户数据目录
├── files                          // 文件
├── lib                            // 第三方库 
├── logs                           // 日志
├── report                         // 测试报告
    └── allure_html                 //测试报告
    └── allure_results              //测试结果
├── scripts                         // 自定义脚本
├── testcases                       //测试用例层
    ├── base                        //接口基础用例，统一平台基础初始化用例，每个用例执行前必执行
        └── usersync.yaml            //用户同步
    ├── bms                          // 接口场景用例
        ├── smokecase                //冒烟用例
        ├── ...                
    ├── features                      // ui场景用例
    ├── step_defs                     // ui步骤函数
    ├── ...
    └── test_api_cases.py             //执行用例
    └── conftest.py                 //用例层前置操作，主要为了解决token问题
    └── extract.yaml                //参数传递文件
    └── case_ceshi.py                //接口自测
├── Readme.md                       
├── pytest.ini  
├── conftest                         // 全局前置操作                 
├── excute.py                       // 运行入口  
├── requirements.txt                            
```

## 接口和ui的融合
### 接口yaml结构

```
# 接口ID
alarminfo_list:
  # 接口基本信息
  ApiInfo:
    # 接口名称
    api_name: 查询告警信息
    # 基础URL:https://192.168.148.174:31000
    base_url: ${base_url}
    # 请求信息
    request:
      # 请求类型
      method: GET
      # 请求地址
      address: /api/auth/v1/monitor/listAlarmInfo
      # 请求头
      headers:
        Content-Type: application/json
        token: ${token}
        Referer: ${base_url}/sub-app-unity/monitor/listAlarmInfo
  # 接口用例，填写接口发送数据、前置操作、后置操作，发送请求时将接口基本信息与接口数据组合
  ApiData:
    # 接口用例ID
    alarminfo_list_01:
      # 接口用例名称
      name: 查询告警信息
      # 接口用例描述
      description: 查询告警信息
      # 请求信息，包括data，file
      request:
        # 请求数据
        data:
          page: 1
          rows: 20
      # 前置操作
      preProcessors:
        # 数据库操作
        database:
          - type: mysql
            sql: update `bms-general-uba`.t_user_source tus set isRemoved = '1' where name like '自动化测试%' and isRemoved = '0' 
          - type: mysql    #数据库类型：mysql
            #sql语句，取返回的第一组数据
            sql: select fingerPrintId from `bms-general-dlpparam`.t_dlp_doc_finger_print tddfp where fingerPrintName like '自动化测试指纹库-服务器导入-挂载%' and isRemoved = '0'
            #sql取值
            sqldata:
              - name: fingerPrintId     #变量名称
                # jsonpath表达式
                jsonpath: $.fingerPrintId
      # 后置操作
      postProcessors:
        # 断言
        assert:
          # 状态码校验
          code: 200
          # 返回值校验
          response: {'statusCode': 0, 'msg': 'success'}
          # jsonpath校验
          jsonpath:
            - path: $.data.list[0].name
              value: 自动化测试70.235数据源
              type: in
          # 数据库校验
          dbcheck:
            - type: mysql
              sql: select count(1) as count from `bms-general-aa`.t_monitor_alarm_rule tmar where  alarmName like '自动化测试' and isEnable ='0' and isRemoved = '0'
              result:
                - path: $.count
                  value: 0        
        # 提取变量
        extract:
          - name: id     #变量名称
            # jsonpath表达式
            jsonpath: $.data.list[0].id
          - name: name     #变量名称
            # jsonpath表达式
            jsonpath: $.data.list[0].name
          - name: token     #变量名称
            # jsonpath表达式
            jsonpath: $.data.token
            # 变量类型：全局变量-global、临时变量-temp（不填写默认为临时变量）
            type: global
        database:
          - type: mysql    #数据库类型：mysql
            #sql语句，取返回的第一组数据
            sql: select * from `bms-general-dlpparam`.t_dlp_doc_finger_print tddfp where fingerPrintName like '自动化测试MD5%' and fingerPrintType = '2' and isRemoved = '0'
            #sql取值
            sqldata:
              - name: fingerPrintId
                jsonpath: $.fingerPrintId     
              - name: id
                jsonpath: $.id 
              - name: fileContent
                jsonpath: $.fileContent
```
#### 取值方式
1. 参数取值：${}
2. 时间取值: $GetTime()
   - 获取当前时间，指定格式：$GetTime(format=%Y-%m-%d %H:%M:%S)
   - 获取当前时间，时间偏移：$GetTime(format=%Y-%m-%d %H:%M:%S;cal=m+1)
     - +：向后偏移；-：向前偏移
     - w：周偏移；d：天偏移；h：小时偏移；m：分钟偏移
3. 表达式计算
   - 取值后，进行公式计算：$Eval(${};cal=+1)
   - 取值后，转换格式，根据jsonpath获取指定值：$Eval(${};path=)  
      （针对获取的值为字符串，需要获取字符串中的特定参数的场景）
4. 参数加密：$Enc()


### UI用例feature结构
```
Feature: 用户及机构管理模块
  用户管理 -> 基础数据管理 -> 用户与机构管理模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：基础数据管理 下的三级菜单：用户与机构管理



  Scenario: ui手动新增用户并使用接口删除用户
    Given 点击按钮：新增
    When 输入新增用户信息：
      | 账号   | 认证方式 | 姓名   | 所属机构 | 职位    |
      | tanglei1 | 口令认证 | tanglei1   | 默认组   | 普通职员 |
    And 点击按钮：确认
    Then 弹出提示框，显示提示信息：新增成功
    Given 监听：
         |  url           |     vars        | json_paths |
         | /api/user/v1/users/1 | displayName,sid | $.data.list[0].displayName,$.data.list[0].sid |
         | /api/auth/v1/roles | id | $.data.list[0].id |

    When 根据查询条件进行用户列表查询：
      """
        {
          "账号": "tanglei1",
          "姓名": "tanglei1"
        }
      """
    When 使用接口：
           | 调用接口          | 接口用例id            | 接口用例路径 |
           | user_delete | user_delete_ui | /bms/user/user_delete.yaml|
```

#### UI用例使用接口规则

**难点**

在[UI用例feature结构](#UI用例feature结构) 该场景使用的删除用户接口中的sid的值是未知的 

**解决方式**

在ui的用户界面搜索用户tanglei，通过监听/api/user/v1/users/1的url的方式，获取到tanglei用户sid的值，在通过extra实现变量的传递，接口获取到sid的值，实现接口删除用户

**功能支持**
- 多个url的监听，例如/api/user/v1/users/1 和 /api/auth/v1/roles
- 多个变量的获取和传递，例如sid，name

**使用规则**
1. 只能使用table的输入形式
1. vars 和 json_paths 的数量要一致
2. json_paths  只能使用jsonpath