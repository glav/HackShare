class QueryStats:
    """
    A class to track query statistics including total queries, pass count, fail count,
    and methods to calculate pass/fail percentages.
    """

    def __init__(self, total_queries=0):
        """
        Initialize the QueryStats object with an optional total number of queries.

        Args:
            total_queries (int): The total number of queries to process
        """
        self.total_queries = total_queries
        self.pass_count = 0
        self.fail_count = 0

    def increment_pass(self):
        """Increment the pass counter by 1"""
        self.pass_count += 1

    def increment_fail(self):
        """Increment the fail counter by 1"""
        self.fail_count += 1

    def get_pass_percentage(self):
        """
        Calculate the percentage of passed queries.

        Returns:
            float: The percentage of passed queries, or 0 if no queries processed
        """
        if self.total_queries == 0:
            return 0
        return (self.pass_count / self.total_queries) * 100

    def get_fail_percentage(self):
        """
        Calculate the percentage of failed queries.

        Returns:
            float: The percentage of failed queries, or 0 if no queries processed
        """
        if self.total_queries == 0:
            return 0
        return (self.fail_count / self.total_queries) * 100

    def get_processed_count(self):
        """
        Get the total number of processed queries (pass + fail).

        Returns:
            int: The total number of processed queries
        """
        return self.pass_count + self.fail_count

    def get_remaining_count(self):
        """
        Get the number of queries that haven't been processed yet.

        Returns:
            int: The number of remaining queries
        """
        return max(0, self.total_queries - self.get_processed_count())

    def get_stats_summary(self):
        """
        Get a dictionary containing all statistics.

        Returns:
            dict: A dictionary with all query statistics
        """
        processed = self.get_processed_count()
        return {
            "total_queries": self.total_queries,
            "processed_queries": processed,
            "remaining_queries": self.get_remaining_count(),
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "pass_percentage": self.get_pass_percentage(),
            "fail_percentage": self.get_fail_percentage(),
            "completion_percentage": (processed / self.total_queries * 100) if self.total_queries > 0 else 0
        }

    def __str__(self):
        """
        String representation of the query statistics.

        Returns:
            str: A formatted string with the statistics
        """
        stats = self.get_stats_summary()
        return (f"Query Statistics:\n"
                f"  Total Queries: {stats['total_queries']}\n"
                f"  Processed: {stats['processed_queries']} ({stats['completion_percentage']:.1f}%)\n"
                f"  Remaining: {stats['remaining_queries']}\n"
                f"  Passed: {stats['pass_count']} ({stats['pass_percentage']:.1f}%)\n"
                f"  Failed: {stats['fail_count']} ({stats['fail_percentage']:.1f}%)")
