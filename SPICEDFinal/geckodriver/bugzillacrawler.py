from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import time
import string
import re
#changing user agents ?
#url/robots.txt

"""cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False"""
driver = webdriver.Firefox(executable_path="/Users/justinburack/Desktop/geckodriver/geckodriver.exe")

priorities = ['P1', 'P2', 'P3', 'P4', 'P5']
severities = ['blocker', 'critical', 'major', 'normal', 'minor', 'trivial']

with open('P5.csv', 'w') as f:
    f.write('ID, Type, Summary, Description, Product, Comp, Assignee, Status, Resolution, Updated, Priority, Severity \n')

for priority in priorities:
    for severity in severities:

        url = 'https://bugzilla.mozilla.org/buglist.cgi?bug_severity=' + str(severity) + '&classification=Client%20Software&classification=Developer%20Infrastructure&classification=Components&classification=Server%20Software&classification=Other&priority=' + str(priority) + '&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0'

        driver.get(url)

        ids = driver.find_elements_by_xpath('//*[@class="first-child bz_id_column"]')
        id_list = []
        for i in range(len(ids)):
            id_list.append(ids[i].text)
        print(len(ids))
        print(len(id_list))
        print(id_list[0:50])

        new_id_list = [id_list[i:i+500] for i in range(0,len(id_list),500)]

        #time.sleep(1200)

        for i in range(len(new_id_list)):
            for j in range(len(new_id_list[i])):
                url = 'https://bugzilla.mozilla.org/show_bug.cgi?id=' + new_id_list[i][j]
                driver.get(url)
                types = driver.find_elements_by_xpath('//*[@id="field-value-bug_type"]/span')
                summaries = driver.find_elements_by_xpath('//h1[@id="field-value-short_desc"]')
                descriptions = driver.find_elements_by_xpath('//*[@id="ct-0"]')
                products = driver.find_elements_by_xpath('//*[@id="product-name"]')
                comps = driver.find_elements_by_xpath('//*[@id="component-name"]')
                assignees = driver.find_elements_by_xpath('//*[@id="field-value-assigned_to"]/div/a/span')
                statuses = driver.find_elements_by_xpath('//*[@id="field-value-status-view"]')
                dates = driver.find_elements_by_xpath('//*[@id="field-value-status_summary"]/span[3]/span[1]/span')
                updates = driver.find_elements_by_xpath('//*[@id="ar-a677_378667"]/td/div/span')
                priorities = driver.find_elements_by_xpath('//*[@id="field-value-priority"]')
                severities = driver.find_elements_by_xpath('//*[@id="field-value-bug_severity"]')

                keys = [new_id_list[i][j], types, summaries, descriptions, products, comps, assignees, statuses, dates, updates, priorities, severities]

                """for key in keys[1:]:
                    try:
                        print(key[0].text)
                    except IndexError:
                        print('Null')"""

                with open('P5.csv', 'a') as f:
                    print(new_id_list[i][j])
                    f.write(new_id_list[i][j] + ',')
                    for key in keys[1:]:
                        try:
                            string = key[0].text

                            f.write(re.sub('(\s+)|(\W+)', ' ', string) + ',')
                        except IndexError:
                            key = 'nan'
                            f.write(key + ',')
                    f.write('\n')


            print('Batch of 500')
            print(len(summaries))

            num = random.randint(300, 600)
            time.sleep(num)
