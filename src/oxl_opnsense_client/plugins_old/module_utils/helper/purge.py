

def purge(
        m, result: dict,
        item_to_purge: dict, diff_param: str, obj_func
) -> None:
    result['changed'] = True

    if m.params['action'] == 'delete':
        result['diff']['before'][item_to_purge[diff_param]] = item_to_purge
        result['diff']['after'][item_to_purge[diff_param]] = None

    else:
        result['diff']['before'][item_to_purge[diff_param]] = {'enabled': True}
        result['diff']['after'][item_to_purge[diff_param]] = {'enabled': False}

    if not m.check_mode:
        _obj = obj_func(item_to_purge)

        if m.params['action'] == 'delete':
            _obj.delete()

        else:
            _obj.b.disable()


def check_purge_filter(m, item: dict) -> bool:
    to_purge = True

    for filter_key, filter_value in m.params['filters'].items():
        if m.params['filter_invert']:
            # purge all except matches
            if m.params['filter_partial']:
                if str(item[filter_key]).find(filter_value) != -1:
                    to_purge = False
                    break

            else:
                if item[filter_key] == filter_value:
                    to_purge = False
                    break

        else:
            # purge only matches
            if m.params['filter_partial']:
                if str(item[filter_key]).find(filter_value) == -1:
                    to_purge = False
                    break

            else:
                if item[filter_key] != filter_value:
                    to_purge = False
                    break

    return to_purge
