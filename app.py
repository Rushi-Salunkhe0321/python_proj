from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

confluence_token = "Your Confluence Token"

req_data = requests.Session()

req_data.headers["Authorization"] = f"Bearer {confluence_token}"

confluence_pages = pd.read_csv("confluence_handoff_pages_last_now_days.csv")

confluence_pages_depth_1 = []
confluence_pages_depth_2 = []
confluence_pages_depth_3 = []
confluence_pages_depth_4 = []
confluence_pages_depth_5 = []

table_rows_val = []

table_headings = ['page_title', 'page_link', 'dependency_no', 'description', 'version', 'importance', 'notes', 'handoff_link_title', 'handoff_link','depth']

parent_pages = confluence_pages["webui"]      
depth_list = [parent_pages, confluence_pages_depth_1, confluence_pages_depth_2, confluence_pages_depth_3, confluence_pages_depth_4, confluence_pages_depth_5]


for i, depth in enumerate(depth_list, start=0):

    if i == 0:
        print("Fetching Parent Page Dependencies")
    else:
        print(f"Fetching Depth {i} Page Dependencies")

    print(f"Total Pages :: {len(depth)}")

    for links in depth:

        url = "https://qwiki.intranet.qualys.com" + links
        
        html_content = req_data.get(url).text
        soup = BeautifulSoup(html_content, "lxml")

        page_title = soup.find("h1", attrs={"id": "title-text"})
        page_title = page_title.get_text(strip=True) if page_title else "N/A"

        table_wraps = soup.find_all("div", attrs={"class": "expand-container conf-macro output-block"}) 
        
        for table_wrap in table_wraps:
            soup = BeautifulSoup(str(table_wrap), "lxml")
            sub_tables = soup.find_all("table", attrs={"class": "relative-table wrapped confluenceTable"}) 
            for sub_table in sub_tables:

                th_data = sub_table.find_all("th")
                headers = [th.get_text(strip=True) for th in th_data]
                
                # print(headers.encode("utf-8"))
                if any(re.search(r'Description', h) for h in headers) and any(re.search(r'Ver', h) for h in headers) and any(re.search(r'Importance', h) for h in headers) and any(re.search(r'Handoff', h) for h in headers):
                    tr_details = sub_table.find_all("tr")
                    
                    for tr in tr_details:
                        # print(tr.encode("utf-8"))
                        row = tr.find_all("td")
                        # for h in row:
                        #     print(h.encode("utf-8"))
                        row_data = [page_title, links]
                        # print(page_title,len(row))
                        
                        if len(row) >= 6:
        
                            dependency_links = row[5].find_all("a")
                            # print(page_title,dependency_links,row)
                            if len(dependency_links) == 0:
                                dependency_links.append("N/A")
                                
                            for dependency_link in dependency_links:
                                # print(page_title,dependency_link,row)
                                row_data = [page_title, links]
                                try:
                                    text = str(row[0].get_text(strip=True)).replace(","," COMMA ")
                                    row_data.append(text[:499])
                                except IndexError as ie:
                                    row_data.append("N/A")
                                try:
                                    text = str(row[1].get_text(strip=True)).replace(","," COMMA ")
                                    row_data.append(text[:499])
                                except IndexError as ie:
                                    row_data.append("N/A")
                                try:
                                    text = str(row[2].get_text(strip=True)).replace(","," COMMA ")
                                    row_data.append(text[:499])
                                except IndexError as ie:
                                        row_data.append("N/A")
                                try:
                                    text = str(row[3].get_text(strip=True)).replace(","," COMMA ")
                                    row_data.append(text[:499])
                                except IndexError as ie:
                                    row_data.append("N/A")
                                try:
                                    text = str(row[4].get_text(strip=True)).replace(","," COMMA ")
                                    row_data.append(text[:499])
                                except IndexError as ie:
                                    row_data.append("N/A")
                                try:
                                    handoff_link = dependency_link.get_text(strip=True)
                                    row_data.append(handoff_link)
                                    extracted_dependency_link = dependency_link.get("href").replace("https://qwiki.intranet.qualys.com","")
                                    # print(extracted_dependency_link)
                                except:
                                    handoff_link = "N/A"
                                    row_data.append("N/A")
                                    extracted_dependency_link = "N/A"

                                if extracted_dependency_link != "N/A" and pd.notna(extracted_dependency_link) and ("/pages/viewpage" in extracted_dependency_link or "/display/HODOC/" in extracted_dependency_link):
                                    row_data.append(extracted_dependency_link)
                                
                                    if extracted_dependency_link not in confluence_pages["webui"].values and extracted_dependency_link not in confluence_pages_depth_1 and extracted_dependency_link not in confluence_pages_depth_2 and extracted_dependency_link not in confluence_pages_depth_3 and extracted_dependency_link not in confluence_pages_depth_4 and extracted_dependency_link not in confluence_pages_depth_5:
                                        print(len(confluence_pages["webui"]),len(confluence_pages_depth_1),len(confluence_pages_depth_2),len(confluence_pages_depth_3),len(confluence_pages_depth_4),len(confluence_pages_depth_5))
                                        if i+1 < 6:
                                            depth_list[i+1].append(extracted_dependency_link)
                                        
                                else:
                                    row_data.append("N/A")  

                                if i == 0:
                                    row_data.append("Parent Page")
                                else:
                                    row_data.append(f"Depth {i}")
                                # print(len(row_data))
                                table_rows_val.append(row_data)
                                # if len(row_data) > 10:
                                    # print(row_data)
                        else:
                            try:
                                text = str(row[0].get_text(strip=True)).replace(","," COMMA ")
                                row_data.append(text[:499])
                            except IndexError as ie:
                                row_data.append("N/A")
                            try:
                                text = str(row[1].get_text(strip=True)).replace(","," COMMA ")
                                row_data.append(text[:499])
                            except IndexError as ie:
                                row_data.append("N/A")
                            try:
                                text = str(row[2].get_text(strip=True)).replace(","," COMMA ")
                                row_data.append(text[:499])
                            except IndexError as ie:
                                row_data.append("N/A")
                            try:
                                text = str(row[3].get_text(strip=True)).replace(","," COMMA ")
                                row_data.append(text[:499])
                            except IndexError as ie:
                                row_data.append("N/A")
                            try:
                                text = str(row[4].get_text(strip=True)).replace(","," COMMA ")
                                row_data.append(text[:499])
                            except IndexError as ie:
                                row_data.append("N/A")
                            try:
                                handoff_link = row[5].get_text(strip=True)
                                row_data.append(handoff_link)
                                extracted_dependency_link = (row[5].find("a").get("href") if row[5].find("a") else "N/A").replace("https://qwiki.intranet.qualys.com","")
                            except IndexError as ie:
                                handoff_link = "N/A"
                                row_data.append("N/A")
                                extracted_dependency_link = "N/A"

                            if extracted_dependency_link != "N/A" and pd.notna(extracted_dependency_link) and ("/pages/viewpage" in extracted_dependency_link or "/display/HODOC/" in extracted_dependency_link):
                                row_data.append(extracted_dependency_link)
                            
                                if extracted_dependency_link not in confluence_pages["webui"].values and extracted_dependency_link not in confluence_pages_depth_1 and extracted_dependency_link not in confluence_pages_depth_2 and extracted_dependency_link not in confluence_pages_depth_3 and extracted_dependency_link not in confluence_pages_depth_4 and extracted_dependency_link not in confluence_pages_depth_5:
                                    print(len(confluence_pages["webui"]),len(confluence_pages_depth_1),len(confluence_pages_depth_2),len(confluence_pages_depth_3),len(confluence_pages_depth_4),len(confluence_pages_depth_5))
                                    if i+1 < 6:
                                        depth_list[i+1].append(extracted_dependency_link)
                                    
                            else:
                                row_data.append("N/A")  

                            if i == 0:
                                row_data.append("Parent Page")
                            else:
                                row_data.append(f"Depth {i}")
                            
                            table_rows_val.append(row_data)
                            # print(len(row_data))


df = pd.DataFrame(data=table_rows_val, columns=table_headings)

df.to_csv("fetch_dependencies.csv", index=False, encoding="utf-8")