from Bio import Entrez
import os
import streamlit as st
from fun import *
# 设置PubMed数据库的邮箱地址
def Download(query,num) :
    Entrez.email = "your_email@example.com"  # 请替换为您的邮箱地址
    print("Here")
    xml_dir = "data"  # 存储XML文件的目录
    # 搜索PubMed数据库
    handle = Entrez.esearch(db="pubmed", term=query, retmax=num)  # 最多检索100篇文章
    record = Entrez.read(handle)
    handle.close()
    if record['IdList'] == None :
        st.markdown("## **No Result **")
    # 下载并保存XML文件
    base_path = os.path.join(xml_dir,query)

    if os.path.isdir(base_path):
        print("目錄存在")
    else:
        print("目錄不存在")
        os.mkdir(os.path.join(base_path))
        os.mkdir(os.path.join(base_path,"xml"))
        os.mkdir(os.path.join(base_path,"pkl"))

    for pubmed_id in record["IdList"]:
        fetch_handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="xml", retmode="xml")
        xml_data = fetch_handle.read()
        fetch_handle.close()

        # 构造XML文件的文件名，通常使用PubMed ID
        xml_file_name = os.path.join(base_path,"xml", f"X{pubmed_id}.xml")

        # 将XML数据保存到文件，使用二进制模式 'wb' 来写入字节数据
        with open(xml_file_name, "wb") as xml_file:
            xml_file.write(xml_data)

        temp = extract_pubmed_info(xml_file_name,query)
        st.markdown("Successful Download !! **PMID:** {}".format(pubmed_id))
        st.markdown("**Title :** {}".format(temp['ArticleTitle']))

    return
