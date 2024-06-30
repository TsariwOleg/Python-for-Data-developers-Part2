import json as js
from datetime import datetime
from typing import List, Union, Dict

from utils.date_utils import parse_date_with_timezone


class Channel:
    """
    Represents a channel in an RSS feed, including metadata and a list of items.

    Attributes:
        source (str): The URL source of the RSS feed.
        title (str): Title of the channel.
        link (str): Link to the channel.
        lastBuildDate (str): The last build date of the channel.
        pubDate (str): Publication date of the channel.
        language (str): Language of the channel.
        category (str): Comma-separated list of categories for the channel.
        managingEditor (str): The managing editor of the channel.
        description (str): Description of the channel.
        item (List[Item]): List of `Item` objects in the channel.
    """

    def __init__(self, source, **kwargs):
        """
        Initialize a new Channel instance.

        Arguments:
            source (str): The source URL of the channel.
            **kwArguments: Arbitrary keyword arguments containing channel attributes.
        """
        self.source = source
        self.title = kwargs.get("title")
        self.link = kwargs.get("link")
        self.lastBuildDate = kwargs.get("lastBuildDate")
        self.pubDate = kwargs.get("pubDate")
        self.language = kwargs.get("language")
        self.category = self.__parse_categories(kwargs.get("category")) if kwargs.get("category") else None
        self.managingEditor = kwargs.get("managingEditor")
        self.description = kwargs.get("description")
        self.item = Item.from_dict(kwargs.get("item")) if kwargs.get("item") else None

    def filter_items(self, date: datetime):
        """
        Filter the items in the channel based on their publication date.

        Arguments:
            date (datetime): The date to filter the items by.

        Returns:
            Channel: The instance of this Channel with filtered items.
        """
        self.item = list(filter(lambda x: x.pubDate and parse_date_with_timezone(x.pubDate).date() == date, self.item))
        return self

    @staticmethod
    def __parse_categories(categories: List[Union[str, dict]]):
        """
        Parse the categories from a list and return them as a comma-separated string.

        Arguments:
            categories (List[Union[str, dict]]): A list of category names or dictionaries containing category details.

        Returns:
            str: Comma-separated category names.
        """
        categories_list = [i if isinstance(i, str) else i.get("#text") for i in categories]
        return ", ".join(categories_list)

    @staticmethod
    def create_output(obj, json, limit):
        """
        Create output from the channel information formatted as JSON or a simple text.

        Arguments:
            obj (Channel): The Channel object to format.
            json (bool): Whether to output as JSON.
            limit (int): Limit the number of items to include in the output.

        Returns:
            str: The formatted channel data as JSON string or list of strings.
        """
        final_dict = Channel.filter_parameters(obj)
        if obj.item:
            final_dict["item"] = [(Channel.filter_parameters(i)) for i in obj.item[:limit]]
        else:
            final_dict["item"] = None

        if json:
            return js.dumps(final_dict, indent=1)
        else:
            return "\n".join(Channel.create_common_output(final_dict))

    @staticmethod
    def create_common_output(final_dict):
        """
        Generate a common output format for channel details as a list of strings.

        Arguments:
            final_dict (Dict): The dictionary containing channel details.

        Returns:
            List[str]: The channel details formatted as a list of strings.
        """
        field_name = {
            "title": "Feed",
            "link": "Link",
            "lastBuildDate": "Last Build Date",
            "pubDate": "Publish Date",
            "language": "Language",
            "category": "Categories",
            "managingEditor": "Editor",
            "description": "Description",
        }

        items = final_dict.pop("item")

        final_list = [f"{field_name.get(k)}: {v}" for k, v in final_dict.items()]
        final_list.append("")

        if items:
            for i in items:
                final_list.extend(Item.create_common_output(i))

        return final_list[:-1]

    @staticmethod
    def filter_parameters(obj):
        """
        Filter out parameters from the Channel object that are not None and are not 'source'.

        Arguments:
            obj (Channel): The Channel object to filter parameters from.

        Returns:
            Dict: A dictionary of filtered parameters.
        """
        return {k: v for k, v in obj.__dict__.items() if v is not None and k != "source"}

    def to_dict(self):
        """
        Convert the Channel object to a dictionary, excluding None values.

        Returns:
            Dict: The Channel object as a dictionary.
        """
        result = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.item:
            result["item"] = [i.to_dict() for i in self.item]
        return result

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Create a Channel object from a dictionary.

        Arguments:
            data (Dict): A dictionary containing channel data.

        Returns:
            Channel: The newly created Channel object.
        """
        if "category" in data and data["category"] is not None:
            data["category"] = data["category"].split(", ")
        return cls(**data)


class Item:
    """
    Represents an item in an RSS feed.

    Attributes:
        title (str): Title of the item.
        author (str): Author of the item.
        pubDate (str): Publication date of the item.
        link (str): URL link to the item.
        category (str): Category of the item.
        description (str): Description of the item.
    """

    def __init__(self, **kwargs):
        """
        Initialize a new Item instance.

        Arguments:
            **kwArguments: Arbitrary keyword arguments containing item attributes.
        """
        self.title = kwargs.get("title")
        self.author = kwargs.get("author")
        self.pubDate = kwargs.get("pubDate")
        self.link = kwargs.get("link")
        self.category = kwargs.get("category")
        self.description = kwargs.get("description")

    @staticmethod
    def create_common_output(final_dict: dict):
        """
        Generate a common output format for item details as a list of strings.

        Arguments:
            final_dict (dict): The dictionary containing item details.

        Returns:
            List[str]: The item details formatted as a list of strings.
        """
        field_name = {
            "title": "Title",
            "author": "Author",
            "pubDate": "Published",
            "link": "Link",
            "category": "Categories",
        }

        final_list = [f"{field_name.get(k)}: {v}" for k, v in final_dict.items() if k != "description"]

        desc = final_dict.get("description")

        if len(final_list) > 1 and desc:
            final_list.append(f"")
        if desc:
            final_list.append(desc)

        final_list.append(f"")

        return final_list

    def to_dict(self):
        """
        Convert the Item object to a dictionary, excluding None values.

        Returns:
            Dict: The Item object as a dictionary.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Create a list of Item objects from a dictionary or list of dictionaries.

        Arguments:
            data (Union[Dict, List[Dict]]): A dictionary or list of dictionaries containing item data.

        Returns:
            List[Item]: A list of newly created Item objects.
        """
        if isinstance(data, dict):
            data = [data]
        return [cls(**i) for i in data]
