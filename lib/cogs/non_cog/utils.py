
import discosnow as ds

def snowflakeToDate(snowflake):
    if not isinstance(snowflake, int):
        return None

    elif snowflake < 4194304:
        return None

    else:
        datetime = ds.snowflake2time(snowflake)
        return str(datetime)

if __name__ == '__main__':
    snowflakeToDate(853338000368599102)
