# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import psycopg2
import re


class CafPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)

            if field_name == 'abstract':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].strip(',')
                    adapter[field_name] = adapter[field_name].lstrip('Abstract')
                    adapter[field_name] = adapter[field_name].lstrip(':')
                    adapter[field_name] = adapter[field_name].lstrip(',')
                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = re.split(r"\s+", adapter[field_name])
                    adapter[field_name] = " ".join(str(elem) for elem in adapter[field_name])
                    adapter[field_name] = adapter[field_name].replace("…", "")
                    adapter[field_name] = adapter[field_name].strip(',')
                    adapter[field_name] = adapter[field_name].lstrip('Abstract')
                    adapter[field_name] = adapter[field_name].lstrip(':')
                    adapter[field_name] = adapter[field_name].lstrip(',')
                    adapter[field_name] = adapter[field_name].strip()


            elif field_name == 'pub_date':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].strip(',')
                    adapter[field_name] = adapter[field_name].strip('[')
                    adapter[field_name] = adapter[field_name].strip(']')
                    adapter[field_name] = adapter[field_name].strip(')')
                    adapter[field_name] = adapter[field_name].strip('(')
                    adapter[field_name] = adapter[field_name].lstrip('Submitted on')
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = datetime.strptime(adapter[field_name], "%d %b %Y")
                    adapter[field_name] = adapter[field_name].date()
                    adapter[field_name] = adapter[field_name].strftime("%d/%m/%Y")

                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = adapter[field_name].strip(',')
                    adapter[field_name] = adapter[field_name].strip('[')
                    adapter[field_name] = adapter[field_name].strip(']')
                    adapter[field_name] = adapter[field_name].strip(')')
                    adapter[field_name] = adapter[field_name].strip('(')
                    adapter[field_name] = adapter[field_name].lstrip('Submitted on')
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = datetime.strptime(adapter[field_name], "%d %b %Y")
                    adapter[field_name] = adapter[field_name].date()
                    adapter[field_name] = adapter[field_name].strftime("%d/%m/%Y")

            elif field_name == 'link':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].strip('{')
                    adapter[field_name] = adapter[field_name].strip('}')

                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = adapter[field_name].strip('{')
                    adapter[field_name] = adapter[field_name].strip('}')

            elif field_name == 'title':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].lstrip('Title')
                    adapter[field_name] = adapter[field_name].lstrip(':')
                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = adapter[field_name].lstrip('Title')
                    adapter[field_name] = adapter[field_name].lstrip(':')

            elif field_name == 'authors':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].lstrip('Authors')
                    adapter[field_name] = adapter[field_name].lstrip(':')
                    adapter[field_name] = adapter[field_name].lstrip(',')
                    adapter[field_name] = ",".join(filter(None, adapter[field_name].split(',')))
                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = re.split(r"\s+", adapter[field_name])
                    adapter[field_name] = "".join(str(elem) for elem in adapter[field_name])
                    adapter[field_name] = adapter[field_name].lstrip('Authors')
                    adapter[field_name] = adapter[field_name].replace(" ", "")
                    adapter[field_name] = adapter[field_name].replace("-", " ")
                    # adapter[field_name] = adapter[field_name].replace("…", "")
                    adapter[field_name] = adapter[field_name].lstrip(':')
                    adapter[field_name] = adapter[field_name].lstrip(',')
                    adapter[field_name] = ", ".join(filter(None, adapter[field_name].split(',')))
                    adapter[field_name] = "".join([i for i in adapter[field_name] if not i.isdigit()])


            elif field_name == 'subjects':
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                    adapter[field_name] = adapter[field_name].lstrip(',')
                    adapter[field_name] = "".join(
                        filter(None, [segment.strip() for segment in adapter[field_name].split(',')]))
                else:
                    adapter[field_name] = "".join(str(elem) for elem in value)
                    adapter[field_name] = adapter[field_name].strip()
                    adapter[field_name] = adapter[field_name].lstrip(',')
                    adapter[field_name] = "".join(
                        filter(None, [segment.strip() for segment in adapter[field_name].split(',')]))
        return item


class SaveToPostgresPipeline:
    def __init__(self):

        # Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'Azerty123$'
        database = 'articles'

        # Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS articles(
            id serial PRIMARY KEY,
            link text,
            pub_date DATE,
            title text,
            authors text,
            abstract text,
            subjects text
        )
        """)
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into articles (
            link, 
            pub_date, 
            title, 
            authors, 
            abstract,
            subjects
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["link"],
            item["pub_date"],
            item["title"],
            item["authors"],
            item["abstract"],
            item["subjects"]
        ))

        # Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):
        # Close cursor & connection to database
        self.cur.close()
        self.connection.close()