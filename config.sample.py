MEMCACHE_SERVERS = [
    ('localhost', 11211),
]

MEMCACHE_REGEX = {
    'key': ur'ITEM (.*) \[(.*); (.*)\]',
    'slab': ur'STAT items:(.*):number',
    'stat': ur"STAT (.*) (.*)\r",
}