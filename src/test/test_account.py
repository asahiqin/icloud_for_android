from pyicloud.services.account import AccountStorage


class TestAccount:
    @property
    def summary_plan(self):
        return {'featureKey': 'cloud.storage', 'summary': {'includedInPlan': True, 'limit': 50, 'limitUnits': 'GIB'}, 'includedWithAccountPurchasedPlan': {'includedInPlan': True, 'limit': 50, 'limitUnits': 'GIB'}, 'includedWithAppleOnePlan': {'includedInPlan': False}, 'includedWithSharedPlan': {'includedInPlan': False}, 'includedWithCompedPlan': {'includedInPlan': False}, 'includedWithManagedPlan': {'includedInPlan': False}}

    @property
    def storage(self):
        return AccountStorage({'storageUsageByMedia': [{'mediaKey': 'photos', 'displayLabel': 'Photos and Videos', 'displayColor': 'ffcc00', 'usageInBytes': 41794426709}, {'mediaKey': 'backup', 'displayLabel': 'Backups', 'displayColor': '5856d6', 'usageInBytes': 27250085}, {'mediaKey': 'docs', 'displayLabel': 'Docs', 'displayColor': 'ff9500', 'usageInBytes': 3810377865}, {'mediaKey': 'mail', 'displayLabel': 'Mail', 'displayColor': '007aff', 'usageInBytes': 26844990}, {'mediaKey': 'messages', 'displayLabel': 'Messages', 'displayColor': '34c759', 'usageInBytes': 7917969}], 'storageUsageInfo': {'compStorageInBytes': 0, 'usedStorageInBytes': 45712319778, 'totalStorageInBytes': 53687091200, 'commerceStorageInBytes': 53687091200}, 'quotaStatus': {'overQuota': False, 'haveMaxQuotaTier': False, 'almost-full': False, 'paidQuota': True}})
