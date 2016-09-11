from django.contrib.admin import AdminSite, site


class RsshubAdminSite(AdminSite):

    site_title = 'Rsshub'
    site_header = 'Rsshub administration'
    index_title = 'Site administration'

    def __init__(self, *args, **kwargs):
        super(RsshubAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)


admin_site = RsshubAdminSite()
