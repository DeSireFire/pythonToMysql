#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2021/4/21
# CreatTIME : 9:21 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

"""
运行结果：
CREATE TABLE `！！！！此处填写表名！！！！` (
  `id` int(25) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id(仅作计数使用不可作为关联依据！)',
  `chembl_id` varchar(648) NOT NULL COMMENT 'chembl_id',
  `chembl_target_type` varchar(648) NOT NULL COMMENT 'chembl_target_type',
  `chembl_target_name` varchar(648) NOT NULL COMMENT 'chembl_target_name',
  `chembl_target_alias` json DEFAULT NULL COMMENT 'chembl_target_alias',
  `chembl_target_organisim` varchar(648) NOT NULL COMMENT 'chembl_target_organisim',
  `chembl_target_classification` json DEFAULT NULL COMMENT 'chembl_target_classification',
  `chembl_drug_name` varchar(648) NOT NULL COMMENT 'chembl_drug_name',
  `chembl_drug` varchar(648) NOT NULL COMMENT 'chembl_drug',
  `guidetopharmacology` varchar(648) NOT NULL COMMENT 'guidetopharmacology',
  `human_protein_atlas` json DEFAULT NULL COMMENT 'human_protein_atlas',
  `open_targets` json DEFAULT NULL COMMENT 'open_targets',
  `chembl_pharos_url` json DEFAULT NULL COMMENT 'chembl_pharos_url',
  `ebi_chembl_url` varchar(648) NOT NULL COMMENT 'ebi_chembl_url',
  `raw_datas` json DEFAULT NULL COMMENT 'raw_datas',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_id` (`id`) USING BTREE,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '采集时间'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='总之就是特别牛逼的一表数据';
"""


def dict2sqlDDL(tempDict: dict):
    result = []
    sql_orm = {
        'dict': "  `{conName}` json DEFAULT NULL COMMENT '{COMMENT}',",
        'list': "  `{conName}` json DEFAULT NULL COMMENT '{COMMENT}',",
        'bool': "  `{conName}` varchar(648) NOT NULL COMMENT '{COMMENT}',",
        # 'NoneType': "  `{conName}` json DEFAULT NULL COMMENT '{COMMENT}',",
        'NoneType': "  `{conName}` text COMMENT '{COMMENT}',",
        # 'str': "  `{conName}` varchar(648) NOT NULL COMMENT '{COMMENT}',",
        'int': "  `{conName}` varchar(648) NOT NULL COMMENT '{COMMENT}',",
        'str': str_to_varchar_text_checker,
        # 'float': "  `{conName}` text COMMENT '{COMMENT}',",
        'float': "  `{conName}` float DEFAULT NULL COMMENT '{COMMENT}',",
    }
    must_sql = {
        0: "CREATE TABLE `！！！！此处填写表名！！！！` (",
        1: "  `id` int(1) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id(仅作计数使用不可作为关联依据！)',",
        "autoEnd0": "  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '采集时间',",
        "autoEnd1": "  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',",
        "autoEnd2": "  PRIMARY KEY (`id`) USING BTREE,",
        "autoEnd3": "  UNIQUE KEY `unique_id` (`id`) USING BTREE,",
        # "End": ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4  COMMENT='总之就是特别牛逼的一表数据';",
        "End": ") ENGINE=InnoDB AUTO_INCREMENT=1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT='总之就是特别牛逼的一表数据'",
    }
    for k, v in tempDict.items():
        typeStr = str(type(v))[8:-2]
        if isinstance(v, str):
            result.append(sql_orm[typeStr](k, v).format(conName=k, COMMENT=k))
        else:
            result.append(sql_orm[typeStr].format(conName=k, COMMENT=k))

    for n, c in must_sql.items():
        if isinstance(n, int):
            result.insert(n, c)
        else:
            # 自动添加到行数末尾
            if "autoEnd" in n:
                result.append(c)
            # 绝对末尾
            if "End" == n and list(must_sql.values()).index(c) == len(list(must_sql.keys()))-1:
                result.insert(len(result), c)

        if "(" not in c and ")" in c:
            # 去掉末尾逗号
            if result[-2][-1] == ",":
                result[-2] = result[-2][0:-1]

    for line in result:
        print(line)

def str_to_varchar_text_checker(tempkey:str, tempStr: str):
    """
    根据传入的值长短，判断sql是使用varchar还是text类型
    :return:
    """
    resStr = ""
    if not tempStr:
        return "  `{conName}` varchar(648) DEFAULT NULL COMMENT '{COMMENT}',"
    lenInt = len(tempStr)

    if lenInt < 648:
        resStr = "  `{conName}` varchar(648) DEFAULT NULL COMMENT '{COMMENT}',"

    if lenInt >= 648:
        resStr = "  `{conName}` text COMMENT '{COMMENT}',"

    if "url" in tempkey:
        resStr = "  `{conName}` text COMMENT '{COMMENT}',"

    if tempStr is None:
        resStr = "  `{conName}` text COMMENT '{COMMENT}',"


    # 字段名称包含id
    if "_id" in tempkey or "id" == tempkey:
        if "NOT NULL" not in resStr:
            if "DEFAULT NULL" in resStr:
                resStr = resStr.replace("DEFAULT NULL", "NOT NULL")
            else:
                resStr = resStr.replace("NULL", "NOT NULL")

    return resStr

if __name__ == '__main__':
    itemDict = {'mesh_heading': 'Multiple Endocrine Neoplasia', 'unique_id': 'D009377', 'mesh_qualifier': 'diagnosis', 'abbreviation': 'DI', 'qualifier_unique_id': 'Q000175', 'md5': '34ced869f196b4700a2248d3cbb45ac3'}
    dict2sqlDDL(itemDict)

