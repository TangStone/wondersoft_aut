# Created by gaojie at 2024-04-23
Feature: 管理员配置模块
  用户管理 -> 权限管理 -> 管理员配置模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：权限管理 下的三级菜单：管理员配置

  Scenario: 导入管理员-填写必填项
    Given 点击按钮：导入管理员
    When 点击按钮：模板下载
    Then 弹出提示框，显示提示信息：下载成功
    When 上传管理员文件：管理员导入.xlsx
    Then 弹出提示框，显示提示信息：导入成功
    When 点击按钮：搜索
    Then 管理员列表中包含：xixi

  Scenario: 管理员列表查询
    When 根据查询条件进行管理员列表查询：
      """
        {
          "登录名": "xixi"
        }
      """

  Scenario Outline: 删除管理员
    When 删除管理员：<登录名>
    And 进入二级菜单：基础数据管理 下的三级菜单：用户与机构管理
    And 删除用户：<登录名>
    Examples:
      | 登录名  |
      | xixi01    |