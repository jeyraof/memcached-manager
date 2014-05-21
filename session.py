# -*- coding: utf-8 -*-

import click
import codecs
from helper import get_pylibmc_client, get_telnet_client, get_re_compiler, send_cmd_to_telnet


@click.group()
def cli():
    pass


@cli.command()
@click.argument('key')
def get(key):
    """
    Get value by key
    """
    key = str(key)
    client = get_pylibmc_client()
    result = client.get(key)
    if result:
        print 'KEY:', key
        print 'VAL:', result
    else:
        click.echo('Error: Not found!')


@cli.command()
@click.argument('key')
def delete(key):
    """
    Delete value by key
    """
    key = str(key)
    client = get_pylibmc_client()
    result = client.delete(key)
    if result:
        print 'KEY:', key
        print 'RES: Deleted!'
    else:
        click.echo('Error: Not found!')


@cli.command()
@click.option('--key', '-k', default='*', help='wildcard supported', show_default=True)
def get_key_list(key):
    """
    Get key list from memcached
    """
    client = get_telnet_client()
    stats_item = send_cmd_to_telnet(client, 'stats items')
    slab_id_list = get_re_compiler('slab').findall(stats_item)

    key_value_list = []
    for slab_id in slab_id_list:
        stats_dump = send_cmd_to_telnet(client, 'stats cachedump %s 0' % slab_id)
        key_value_once = get_re_compiler('key').findall(stats_dump)
        key_value_list.append(key_value_once)

    with codecs.open('key_list.txt', mode='w', encoding='utf-8') as f:
        for list_of_list in key_value_list:
            for key_value in list_of_list:
                f.write('%s:%s:%s\n' % tuple(key_value))

    print 'Success! Open key_list.txt'
    client.close()


if __name__ == '__main__':
    cli()