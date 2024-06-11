# Created by gaojie at 2024-04-28
Feature: 文件MD5
  规则管理 -> 基础规则 -> 文件MD5模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：规则管理
    And 进入二级菜单：基础规则 下的三级菜单：文件MD5

  Scenario: 新增文件MD5规则
    Given 点击按钮：导入
    When 输入MD5规则导入信息：
      """
        {
          "是否覆盖现有文件MD5名称": "否",
          "文件MD5名称": "测试-MD5",
          "文件": "MD5-demo.json"
        }
      """
    Then 弹出提示框，显示提示信息：上传成功

  Scenario: 文件MD5查询
    When 根据查询条件进行文件MD5查询：
      """
        {
          "名称": "测试-MD5"
        }
      """

  Scenario Outline: 删除文件MD5
    When 删除文件MD5：<MD5名称>
    Examples:
      | MD5名称  |
      | 测试-MD5 |