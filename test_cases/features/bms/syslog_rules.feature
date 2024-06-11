# Created by gaojie at 2024-04-26
Feature: Syslog规则配置模块
  系统管理 -> 运维管理 -> Syslog规则配置模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：系统管理
    And 进入二级菜单：运维管理 下的三级菜单：Syslog规则配置

  Scenario: 新增syslog规则配置
    Given 点击按钮：新增规则配置
    When 输入新增syslog规则信息：
      """
      {
          "规则名称": "syslog规则",
          "Syslog地址": "192.168.1.1",
          "传输协议": "TCP",
          "Syslog等级": "ERR",
          "Syslog类型": "user(用户进程)",
          "字符编码": "UTF-8编码",
          "自定义分隔符": "/",
          "日志前缀": "log-",
          "时间格式": "yyyy-MM",
          "Syslog应用": ["统一基础平台", "审计日志"],
          "Syslog字段": "全选"
      }
      """
    And 点击【新增规则配置】页面的【确认】按钮
    Then 弹出提示框，显示提示信息：新增成功

  Scenario: syslog规则列表查询
    When 根据查询条件进行syslog规则列表查询：
      """
        {
          "规则名称": "syslog规则"
        }
      """

  Scenario Outline: 删除syslog规则
    When 删除syslog规则：<规则名称>
    Examples:
      | 规则名称    |
      | syslog规则 |