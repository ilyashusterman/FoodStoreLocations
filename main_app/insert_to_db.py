import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodStore.settings")

application = get_wsgi_application()
from main_app.models import Chains
from main_app.models import Branches

MIN_ROWS = 3000

def create_branch(chain_id, name, long, lat):
    return Branches(chain_id=chain_id, name=name,
                    latitude=lat,
                    longitude=long)


def create_chain(name):
    return Chains(name=name)


def get_chains_commands(command):
    inserts = command.split('INSERT INTO `chains` (`id`, `name`) VALUES')[1]
    inserts = inserts.split('),')
    chains = []
    for insert in inserts:
        values = insert.split(", '")
        name = values[1].split("'")[0]
        chain = {
            'table': 'chains',
            'name': name
        }
        chains.append(chain)
    return chains


def get_branches_commands(command):
    inserts = command.split(
        'INSERT INTO `branches` (`id`, `chain_id`, `name`, `longitude`, `latitude`) VALUES')[
        1]
    inserts = inserts.split('),')
    branches = []
    for insert in inserts:
        # values = insert.split(", '")
        row = insert.split(',')[1:]
        # print('row={}'.format(row))
        longit = clean_float(row[2])
        lat = clean_float(row[3])
        name = row[1]
        chain_id = int(row[0].replace(' ', ''))
        check_values_validation(chain_id, lat, longit, name)
        branch = {
            'table': 'branches',
            'name': name,
            'chain_id': chain_id,
            'long': longit,
            'lat': lat
        }
        branches.append(branch)
    return branches


def check_values_validation(chain_id, lat, longit, name):
    assert isinstance(chain_id, int)
    assert isinstance(name, str)
    assert isinstance(lat, float)
    assert isinstance(longit, float)


def clean_float(num):
    return float(num.replace(' ', '').replace("'", '').replace(')', ''))


def get_sql_rows():
    fd = open('test.sql', 'r')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(';')
    chains = []
    branches = []
    for command in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        if 'INSERT INTO `chains` (`id`, `name`) VALUES' in command:
            chains = get_chains_commands(command)[:MIN_ROWS]

        elif 'INSERT INTO `branches` (`id`, `chain_id`, `name`, `longitude`, `latitude`) VALUES' in command:
            branches = get_branches_commands(command)[:MIN_ROWS]

    entities = chains + branches
    return entities


def main():
    for row in get_sql_rows():
        entity = None
        if row['table'] == 'chains':
            entity = create_chain(row['name'])
        elif row['table'] == 'branches':
            entity = create_branch(row['chain_id'], row['name'],
                                   row['long'], row['lat'])
        if entity is not None:
            entity.save()
            print('added row={}'.format(row))


if __name__ == '__main__':
    main()
