from django.core.serializers.json import DjangoJSONEncoder


class PlayerSerializer(DjangoJSONEncoder):
    """
    Custom JSON serializer for the Player model.
    """

    @staticmethod
    def serialize(player):
        """
        Serialize the Player instance as JSON.

        Parameters
        ----------
        player : Player
            An instance of the Player model.

        Returns
        -------
        dict
            A dictionary representation of the Player instance.
        """
        return {
            "id": player.id,
            "name": player.name,
            "cfc_id": player.cfc_id,
            "created_at": player.created_at.strftime("%Y-%m-%d %H:%M:%S") if player.created_at else None,
            "updated_at": player.updated_at.strftime("%Y-%m-%d %H:%M:%S") if player.updated_at else None,
        }
